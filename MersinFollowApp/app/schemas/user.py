from pydantic import BaseModel, EmailStr, Field
from enum import Enum

class Gender(str, Enum):
    male = "male"
    female = "female"

class Role(str, Enum):  # NEW
    admin = "admin"
    user = "user"

class UserCreate(BaseModel):
    first_name: str = Field(min_length=1, max_length=50)
    last_name: str = Field(min_length=1, max_length=50)
    email: EmailStr
    password: str = Field(min_length=6)
    gender: Gender
    role: Role = Role.user
    server_token: str | None = None  # Admin panelinden/set edilebilir

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    gender: Gender
    role: Role
    server_token: str | None

    class Config:
        from_attributes = True  # SQLAlchemy objesinden okunabilsin

class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
