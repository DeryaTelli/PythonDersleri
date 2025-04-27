from typing import Annotated

from aiohttp.abc import HTTPException
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from sqlalchemy.util import deprecated
from starlette import status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

from database import SessionLocal
from models import User

#router mantigi
# bir klasor olusturup end pointerli kapsayan tum islemleri bir dosya icinde toplar
# icinde bir tane app oluyor onlari yolluyor farkli end pointler tek bir app icerisinde yer alabiliyor


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency=Annotated[Session, Depends(get_db)]
bcrypt_context=CryptContext(schemes=["bcrypt"], deprecated="auto")


class CreateUserRequest(BaseModel):
    username:str
    email:str
    first_name: str
    last_name:str
    password:str
    role:str

def authenticate_user(username:str, password:str,db):
    user=db.query(User).filter(User.username==username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password,user.hashed_password):
        return False
        #verify ile kullanicin sifresi ile database kaydedilen hash kod aynimi onu kontrol ediyoruz
    return user


#alt enter diyip import et
@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(db:db_dependency , create_user_request: CreateUserRequest):
    user=User(
        username=create_user_request.username,
        email=create_user_request.email,
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        role=create_user_request.role,
        is_active=True,
        hashed_password=bcrypt_context.hash(create_user_request.password)
    )
    db.add(user)
    db.commit()

#token: kullanici giris yaptiginda kullanicita token veriyoruz istek olarak atiyoruz
# kullanici icin ona ozel olustrudugmuz bir token guvenlik icin kullaniyoruz

@router.post("/token")
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm,Depends()], db:db_dependency):
    user=authenticate_user(form_data.username,form_data.password,db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="incorrect username or password")
    token=""
    return {"access_token":token, "token_type":"bearer"}

#JWT Token Ne Demek?
#JWT, "JSON Web Token" demektir.
#JWT, bir kullanıcıyı güvenli şekilde tanımlamak
# veya bilgi taşımak için kullanılan dijital
# bir kimlik kartı gibi bir şeydir.