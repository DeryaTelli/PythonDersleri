from fastapi import FastAPI

app=FastAPI()

#endpoint
# herbir endpoint olustururken fonksiyon tanimlamamiz gerekir


#asenkron bir sekilde calismamiz gerekir bir suru istek gidip gelir
@app.get("/hello")
#farkli pathlari buradan tanimliyoruz /helloya gidince bu message degerimi gorecektir
async def hello_world():
    return {"message": "hello world"}
# return message dictinary dir json tarzi icin bu sekilde kullanilir
# JSON (javascript object notation) nedir
# veriyi ilettmek icin kullanilan gosterim yani dosya formati



#terminalden su sekilde calistiriyoruz kodu
# ilk olarak pip install uvicorn[standart] indiriyoruz
# calistirmak icinde uvicorn main:app --reload diyoruz
# farkli calistirma yolu fastapi run main.py
# calistirmayi kapatmak istersek CTRL+C tikliyoruz
# pip freeze dedigimizde fast apinin kutuphaneyi kendi yukledigini gorceksiniz


#crap nedir
#crapin acilimi ve http methodlariyla eslesmesi  create(post) , read(get), update(put)  delete(delete)
# http methodlari var client ve server tarafinda
# http methodlari :get,post,put,head,delete,patch,options,connect,trace
# sunucudan okuma islemi yapmak istiyorsak get kullanabilirz


