from pydantic import BaseModel, EmailStr, Field


class UserAuth(BaseModel):
    username: str
    password: str = Field(min_length=8)


class AuthResponse(BaseModel):
    access_token:str
    token_type:str





