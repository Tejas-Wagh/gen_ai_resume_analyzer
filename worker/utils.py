from io import BytesIO
from services import get_s3_client
from pypdf import PdfReader
import os
from custom_agents import resume_analyzer_agent, email_agent
from agents import Runner
from contextlib import contextmanager
from core.database import SessionLocal
from core.models import AnalysisHistory, User



@contextmanager
def db_session():
    db = SessionLocal()

    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()



def fetch_pdf_from_s3( key:str):
    buffer = BytesIO()
    s3 = get_s3_client()
    s3.download_fileobj(os.getenv("BUCKET_NAME"), key, buffer)
    buffer.seek(0)
    return buffer  


def extract_text_from_pdf(file_obj: BytesIO):
    reader = PdfReader(file_obj)

    text = []
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text.append(page_text)

    return "\n".join(text)


def generate_response(resume_text):
    result = Runner.run_sync(resume_analyzer_agent, resume_text)
    return result.final_output

def send_email_notification(message, user_email):
   response = Runner.run_sync(email_agent, f"Send to {user_email}: {message}")
   return response.final_output


def save_response(result: str, resume_name: str):
    with db_session() as db:
        resume = db.query(AnalysisHistory).filter(AnalysisHistory.resume_name == resume_name).first()

        if not resume:
            raise ValueError(f"Resume not found: {resume_name}")

        user = db.query(User).filter(User.id == resume.user_id).first()
        
        if not user:
            raise ValueError(f"User not found for resume: {resume_name}")
        
        resume.analysis_result = result
        resume.analysis_status = "completed"

        db.add(resume)
        
        return user.email

