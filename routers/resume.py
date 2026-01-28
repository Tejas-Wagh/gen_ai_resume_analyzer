from fastapi import APIRouter
import os
import uuid
from fastapi import File, UploadFile
from core.models import AnalysisHistory
from core.database import db_dependency
from services import get_s3_client, get_redis_client
from utils import user_dependancy
from fastapi import HTTPException

router = APIRouter(
    prefix="/resume",
    tags=["Resume"],
)

r = get_redis_client()
s3 = get_s3_client()


@router.post("/upload")
def upload_file(db : db_dependency, user: user_dependancy, file: UploadFile = File(...)):

    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    file_name = f"{uuid.uuid4()}_{file.filename}"

    s3.upload_fileobj(
        Fileobj=file.file,
        Bucket=os.getenv("BUCKET_NAME"),
        Key=f"{file_name}",
        ExtraArgs={
            "ContentType": file.content_type
             }
        )
    
  

    new_resume = AnalysisHistory(
        resume_name = file_name,
        user_id = user.get('id'),       
   )
    
    db.add(new_resume)
    db.commit()
    r.lpush("file_key",f"{file_name}")
    
    return {"message": "File Uploaded!", "file_name" : file_name}




@router.get("/result/{resume_name}")
def get_resume_status(resume_name: str, db:db_dependency,  user: user_dependancy):
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
     
    resume = db.query(AnalysisHistory).filter(AnalysisHistory.resume_name == resume_name).first()
    
    if not resume:
        return {"error": "Resume not found"}
    
    if resume.analysis_status == "Pending":
        return {
            "status":"In progress"
        }
    
    return {
        "status": "completed",
        "data" : resume.analysis_result
    }


