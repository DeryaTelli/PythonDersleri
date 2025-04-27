from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from jose.constants import ALGORITHMS
from pydantic import BaseModel
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from sqlalchemy.util import deprecated
from starlette import status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from database import SessionLocal
from models import User
from jose import jwt, JWTError
from datetime import timedelta,datetime,timezone

#router mantigi
# bir klasor olusturup end pointerli kapsayan tum islemleri bir dosya icinde toplar
# icinde bir tane app oluyor onlari yolluyor farkli end pointler tek bir app icerisinde yer alabiliyor


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)

SECRET_KEY="ij2cgacxohygmlhfbs3l0oa9dbrx1wl8"
ALGORITHMS="HS256"

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency=Annotated[Session, Depends(get_db)]
bcrypt_context=CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer=OAuth2PasswordBearer(tokenUrl="/auth/token")


class CreateUserRequest(BaseModel):
    username:str
    email:str
    first_name: str
    last_name:str
    password:str
    role:str
    phone_number:str

class Token(BaseModel):
    access_token:str
    token_type:str


#encoding kismi jwtnin
def create_access_token(username:str, user_id:int, role:str,expires_delta:timedelta):
    encode={'sub':username, 'id':user_id, 'role':role}
    expires=datetime.now(timezone.utc)+expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHMS)

#decoding kismi jwtnin
async def get_current_user(token:Annotated[str,Depends(oauth2_bearer)]):
    try:
        encode=jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHMS])
        username=encode.get('sub')
        user_id=encode.get('id')
        user_role=encode.get('role')
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Username or Id is  invalid")
        return {'username':username, 'id':user_id, 'user_role':user_role}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is invalid")



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
        hashed_password=bcrypt_context.hash(create_user_request.password),
        phone_number=create_user_request.phone_number
    )
    db.add(user)
    db.commit()

#token: kullanici giris yaptiginda kullanicita token veriyoruz istek olarak atiyoruz
# kullanici icin ona ozel olustrudugmuz bir token guvenlik icin kullaniyoruz

@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm,Depends()], db:db_dependency):
    user=authenticate_user(form_data.username,form_data.password,db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="incorrect username or password")
    token = create_access_token(user.username, user.id, user.role, timedelta(minutes=60))
    return {"access_token":token, "token_type":"bearer"}

#JWT Token Ne Demek?
#JWT, "JSON Web Token" demektir.
#JWT, bir kullanıcıyı güvenli şekilde tanımlamak
# veya bilgi taşımak için kullanılan dijital
# bir kimlik kartı gibi bir şeydir.