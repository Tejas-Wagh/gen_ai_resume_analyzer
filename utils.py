from io import BytesIO
from services import get_s3_client
from pypdf import PdfReader
import os
from custom_agents import resume_analyzer_agent, email_agent
from agents import Runner

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

def send_email_notification(message):
   response = Runner.run_sync(email_agent, message)
   return response.final_output