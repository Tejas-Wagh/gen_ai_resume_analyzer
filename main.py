from fastapi import FastAPI, File, UploadFile
from dotenv import load_dotenv
from services import get_s3_client, get_redis_client
import os
import uuid

load_dotenv()
r = get_redis_client()
s3 = get_s3_client()
app = FastAPI()


@app.get("/")
def hello():
    return {"message": "Hello from ai-resume-analyzer!"}



@app.post("/upload")
def upload_file(file: UploadFile = File(...)):
    file_ext = os.path.splitext(file.filename)[1]
    file_name = f"{uuid.uuid4()}{file_ext}"

    s3.upload_fileobj(
        Fileobj=file.file,
        Bucket=os.getenv("BUCKET_NAME"),
        Key=f"uploads/{file_name}",
        ExtraArgs={
            "ContentType": file.content_type
             }
        )
    
    r.lpush("file_key",f"uploads/{file_name}")
    

    return {"message": "File Uploaded!"}



@app.get("/file")
def get_file():
    response = s3.list_objects_v2(
    Bucket="test-resume-analyzer-bucket",
    Prefix="uploads/"
    )

    file = response["Contents"]

    print(response)

    return "hello"

