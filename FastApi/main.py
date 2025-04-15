from fastapi import FastAPI

app=FastAPI()

#endpoint
# herbir endpoint olustururken fonksiyon tanimlamamiz gerekir


#asenkron bir sekilde calismamiz gerekir bir suru istek gidip gelir
@app.get("/hello")
#farkli pathlari buradan tanimliyoruz /helloya gidince bu message degerimi gorecektir
async def hello_world():
    return {"message": "hello world"}

#terminalden su sekilde calistiriyoruz kodu
# ilk olarak pip install uvicorn[standart] indiriyoruz
# calistirmak icinde uvicorn main:app --reload diyoruz
# farkli calistirma yolu fastapi run main.py
# calistirmayi kapatmak istersek CTRL+C tikliyoruz
# pip freeze dedigimizde fast apinin kutuphaneyi kendi yukledigini gorceksiniz


