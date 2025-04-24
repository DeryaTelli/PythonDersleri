from fastapi import FastAPI , Depends
from typing import Annotated
app = FastAPI()

#dependency Injection Nedir?
#Dependency Injection, bir sınıfın (veya fonksiyonun)
# ihtiyaç duyduğu nesneleri dışarıdan alması prensibidir.
# Yani, bir şeyin ihtiyaç duyduğu bağımlılıkları
# kendi içinde oluşturmak yerine, onu dışarıdan sağlarız.


def hello_world():
    return "Hello welcome to FastAPI!"

HelloDependency = Annotated[str:Depends(hello_world)]

#def get_hello_world(hello: str=Depends(hello_world)):
def get_hello_world(hello: HelloDependency):
    #return f"Hello world service: {hello_world()}"
    return f"Hello world service: {hello}"


@app.get("/hello")
def hello(message: str=Depends(get_hello_world)):
    return {"message":message}

#hepsi birbirine bagli bir fonksiyon olusturmus oluyoruz