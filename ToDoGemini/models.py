from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey


class Todo(Base):
    __tablename__='todos'
    id=Column(Integer,primary_key=True, index=True)
    title=Column(String)
    description=Column(String)
    priority=Column(Integer)
    complete=Column(Boolean, default=False)
    owner_id=Column(Integer, ForeignKey('users.id'))

#migration database tablosu olusturulduktan sonra
#ayni tabloda bir sey olustururken yada silerken veritabanimiz anlik olarak guncellenmiyor
# ona kodda yaptigimz degisikliklerin uygulanmasi icin migration kullaniyoruz

class User(Base):
    __tablename__='users'
    id=Column(Integer, primary_key=True, index=True)
    email=Column(String, unique=True)
    username=Column(String, unique=True)
    first_name=Column(String)
    last_name=Column(String)
    hashed_password=Column(String)
    is_active=Column(Boolean , default=True)
    role=Column(String)
    phone_number=Column(String)


