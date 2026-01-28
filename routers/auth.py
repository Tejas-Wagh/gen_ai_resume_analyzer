from fastapi import APIRouter, HTTPException, status as status_code, Depends
from core.database import db_dependency
from core.models import User
from core.types import UserAuth, AuthResponse
from passlib.context import CryptContext
from utils import create_access_token, user_dependancy
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)

bcrypt_ctx = CryptContext(schemes=['bcrypt'])


@router.post("/sign-up")
def sign_up(user:UserAuth, db:db_dependency) -> AuthResponse:
    db_user = db.query(User).filter(User.email == user.username).first()

    if db_user:
        raise HTTPException(status_code=status_code.HTTP_409_CONFLICT, detail="User already available")
    

    hashed_pw =  bcrypt_ctx.hash(user.password)

    new_user =  User(
        email = user.username,
        password = hashed_pw
    )

    db.add(new_user)

    db.commit()

    token = create_access_token(new_user.id, new_user.email)

    return {
        "access_token":token,
        "token_type": "bearer"
    }

    

@router.post("/sign-in")
def sign_in( db:db_dependency, user: OAuth2PasswordRequestForm = Depends()) -> AuthResponse: 
    db_user = db.query(User).filter(User.email == user.username).first()

    if not db_user:
        raise HTTPException(status_code=status_code.HTTP_401_UNAUTHORIZED, detail="User not found")
    
    if not bcrypt_ctx.verify(user.password, db_user.password):
        raise HTTPException(status_code= status_code.HTTP_401_UNAUTHORIZED, detail= "Unauthorized Access!")
    
    token = create_access_token(db_user.id, db_user.email)

    return {
        "access_token":token,
        "token_type": "bearer"  
    }


@router.get("/user")
def get_current_user_details(db:db_dependency, user:user_dependancy ):
    db_user = db.query(User).filter(User.id == user.id).first()

    if not db_user:
        raise HTTPException(status_code=status_code.HTTP_401_UNAUTHORIZED, detail="User not found")
    
    return {
        "id":db_user.id,
        "email": db_user.email
    }

    