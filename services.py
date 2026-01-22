import os
import boto3
import redis
from dotenv import load_dotenv

load_dotenv()

s3 = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("S3_ACCESS_KEY"),
    aws_secret_access_key=os.getenv("S3_SECRET_ACCESS_KEY"),
    region_name="us-east-1"
)


def get_s3_client():
    return s3

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

def get_redis_client():
    return r