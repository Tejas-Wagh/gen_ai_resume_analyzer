from fastapi import FastAPI
from dotenv import load_dotenv
from routers.auth import router as authRouter
from routers.resume import router as resumeRouter

load_dotenv()

app = FastAPI()

@app.get("/")
def hello():
    return {"message": "Hello from ai-resume-analyzer!"}


app.include_router(authRouter)
app.include_router(resumeRouter)






