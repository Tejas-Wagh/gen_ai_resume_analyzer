import os
from jose import jwt, JWTError
from typing import Annotated
from fastapi import Depends, HTTPException, status as status_code
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated


oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/sign-in")

def create_access_token(id:int, email:str):
    data = {
        "sub":email,
        "id":id
    }

    token = jwt.encode(data, os.getenv("JWT_SECRET_KEY"))

    return token
    

def verify_access_token(token : Annotated[str, Depends(oauth2_bearer)]):
    
    try:
        payload = jwt.decode(token, os.getenv("JWT_SECRET_KEY"))

        email = payload.get('sub')
        id = payload.get('id')

        if not email or not id:
            raise HTTPException(status_code=status_code.HTTP_401_UNAUTHORIZED, detail="Could not validate user")
        
        return {
            "email" : email,
            "id": id
        }
    
    except JWTError:
        raise HTTPException(status_code=status_code.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    



user_dependancy = Annotated[dict, Depends(verify_access_token)]