import logging
from starlette.responses import RedirectResponse
logging.basicConfig(level=logging.DEBUG)
from fastapi import FastAPI , Request
from  models import Base
from database import engine
from routers.auth import router as auth_router
from routers.todo import router as todo_router
from fastapi.staticfiles import StaticFiles
from starlette import status

app=FastAPI()
app.mount("/static", StaticFiles(directory="static"),name="static")

#ana app girenlerin nereye gitmesi gerektigi gosteriyoruz bu kodla
@app.get("/")
def read_root(request:Request):
    return RedirectResponse(url="/todo/todo_page", status_code=status.HTTP_302_FOUND)

app.include_router(auth_router)
app.include_router(todo_router)


Base.metadata.create_all(bind=engine)

