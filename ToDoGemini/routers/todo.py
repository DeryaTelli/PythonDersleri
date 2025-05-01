from fastapi import APIRouter , Depends, HTTPException, Path ,Request
from starlette.responses import Response
from pydantic import Field
from pydantic import BaseModel
from starlette import status
from  ..models import Base, Todo
from sqlalchemy.orm import Session
from ..database import engine, SessionLocal
#database baglantisi sagliyoruz sessionlocal kullanarak
from typing import Annotated
from ..routers.auth import get_current_user
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse
from dotenv import load_dotenv
# env dosyalarinin icindekileri kullanmamizi sagliyor
import google.generativeai as genai
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage
import  markdown
from bs4 import BeautifulSoup





router=APIRouter(
    prefix="/todo",
    tags=["Todo"]
)
templates=Jinja2Templates(directory="app/templates")

class TodoRequest(BaseModel):
    # alt enter ile import islemi yapabilirsin
    title: str=Field(min_length=3)
    description: str=Field(min_length=3,max_length=1000)
    priority:int=Field(gt=0,lt=6)
    complete:bool


def get_db():
    db=SessionLocal()
    try:
        yield db
        #return gibidir yield yield kullanan fonksiyonlara generative fonksiyon diyoruz
    finally:
        db.close()
        #islem bittiginde baglantyi kapatmak icni kullaniyorz

db_dependency=Annotated[Session, Depends(get_db)]
#veri tabani icin baglanti sagliyor ve surekli ayni seyi yazmak yerine degisken olusturup bu sekilde kullanmak daha mantikli
user_dependency=Annotated[dict, Depends(get_current_user)]


def redirect_to_login():
    redirect_response=RedirectResponse(url="/auth/login_page", status_code=status.HTTP_302_FOUND)
    redirect_response.delete_cookie("access_token")
    #token eslesmemesi oldugu zaman o token silinip yeni token atanmasi icin yapiyom
    return redirect_response




@router.get("/todo_page")
async def render_todo_page(request:Request, db:db_dependency):
    try:
        user=await get_current_user(request.cookies.get('access_token'))
        #kullanicinin giris yaptigi sayfada verilen token cookiye ekliyoruz
        if user is None:
            return redirect_to_login()
        todos=db.query(Todo).filter(Todo.owner_id==user.get('id')).all()
        return templates.TemplateResponse("todo.html",{"request":request, "todos":todos, "user":user})
    except:
        return redirect_to_login()

#add todo
@router.get("/add_todo_page")
async def render_add_todo_page(request:Request):
    try:
        user=await get_current_user(request.cookies.get('access_token'))
        #kullanicinin giris yaptigi sayfada verilen token cookiye ekliyoruz
        if user is None:
            return redirect_to_login()
        return templates.TemplateResponse("add-todo.html",{"request":request,  "user":user})
    except:
        return redirect_to_login()

#edit todo degisim yaparken path parametresi kullaniyoruz id almak icin
@router.get("/edit_todo_page/{todo_id}")
async def render_todo_page(request:Request,todo_id:int, db:db_dependency):
    try:
        user=await get_current_user(request.cookies.get('access_token'))
        #kullanicinin giris yaptigi sayfada verilen token cookiye ekliyoruz
        if user is None:
            return redirect_to_login()
        todo=db.query(Todo).filter(Todo.id==todo_id).first()
        return templates.TemplateResponse("edit-todo.html",{"request":request, "todo":todo, "user":user})
        # edit-todo yaptigimizda hata veriyorsa hala onu edit_todo yap suan guncellemiyo
    except:
        return redirect_to_login()


@router.get("/")
async def read_all(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return db.query(Todo).filter(Todo.owner_id==user.get('id')).all()


@router.get("/todo/{todo_id}", status_code=status.HTTP_200_OK)
async def read_by_id(user:user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    todo = db.query(Todo).filter(Todo.id == todo_id).filter(Todo.owner_id==user.get('id')).first()
    # tek bir todo vermiyor olurda birden fazla todo geliyorsa liste donduruyor ilk id aliyor ondan
    if todo is not None:
        return todo
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_todo(user:user_dependency, db: db_dependency, todo_request: TodoRequest):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    todo = Todo(**todo_request.dict(), owner_id=user.get('id'))
    todo.description=create_todo_with_gemini(todo.description)
    db.add(todo)
    db.commit()
    db.refresh(todo)  # ID gibi alanları günceller
   # return todo  # Eklenen veriyi döndür
    #db.commit islemin yapilacagi anlamina geliyor eger eklemezseniz islem yapilmaz


@router.put("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async  def update_todo(user: user_dependency,
                       db: db_dependency,
                       todo_request: TodoRequest,
                       todo_id : int =Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    todo = db.query(Todo).filter(Todo.id == todo_id).filter(Todo.owner_id == user.get('id')).first()
    if todo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    todo.title=todo_request.title
    todo.description=todo_request.description
    todo.priority=todo_request.priority
    todo.complete=todo_request.complete
    db.add(todo)
    db.commit()

@router.delete("/todo/{todo_id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(user:user_dependency, db:db_dependency, todo_id:int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    todo = db.query(Todo).filter(Todo.id == todo_id).filter(Todo.owner_id == user.get('id')).first()
    if todo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    db.query(Todo).filter(Todo.id==todo_id).delete()
    #db.delete(todo) calisir yukaridakki kodda calistir
    db.commit()


def markdown_to_text(markdown_string):
    html=markdown.markdown(markdown_string)
    soup=BeautifulSoup(html,"html.parser")
    text=soup.get_text()
    return text


def create_todo_with_gemini(todo_string:str):
    load_dotenv()
    genai.configure(api_key=os.environ.get('GOOGLE_API_KEY'))
    llm = ChatGoogleGenerativeAI(model="gemini-pro")
    response=llm.invoke(
        #istedigim mesajlari buraya dizi olarak verebiliyorum
        [
            HumanMessage(content="I will provide you a todo item to add my to do list. What i want to do is to create a longer and more comprehensive description of that todo item, my next message will be my todo:"),
            HumanMessage(content=todo_string)
        ]
    )
    return markdown_to_text(response.content)

if __name__=="__main__":
    print(create_todo_with_gemini("learn python"))