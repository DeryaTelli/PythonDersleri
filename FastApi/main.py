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

courses_db=[
    {'id': 1, 'instructor': 'Derya', 'title': 'Python', 'category': 'Development'},
    {'id': 2, 'instructor': 'Mehmet', 'title': 'JavaScript', 'category': 'Web Development'},
    {'id': 3, 'instructor': 'Asli', 'title': 'DataScience', 'category': 'Development'},
    {'id': 4, 'instructor': 'Ali', 'title': 'MachineLearning', 'category': 'cloud'},
    {'id': 5, 'instructor': 'Zeynep', 'title': 'React', 'category': 'cloud'},
    {'id': 6, 'instructor': 'Can', 'title': 'Docker', 'category': 'DevOps'},
    {'id': 7, 'instructor': 'Derya', 'title': 'Java', 'category': 'Development'},

]

@app.get("/courses")
async def get_all_courses():
    return courses_db

#/docs yazarsak api ile kullandigim tum methodlari gorurum

#path parameter
# filtre kullanarak nasil deger cekeriz path veya query kullaniriz
# dinamik bir path yapmak istiyorsak onu degisken gibi kabul edecegini var sayiyoruz ve suslu parantez icini aliyoruz
@app.get("/courses/{course_title}")
async def get_course(course_title: str):
    for course in courses_db:
        if course.get('title').casefold() == course_title.casefold():
            return course
# burada ayni olma olaylarinda buyuk harf kucuk harf duyarli olabilir ya lower(),upper() yada casefold() kullaniriz


#path cakismasi
@app.get("/courses/{course_id}")
async def get_course_by_id(course_id:int):
    for id in courses_db:
        if id.get('id')== course_id:
            return id

# course title id olarak degistirsekde id tarama yaparken null deger verecektir
# bunun sebebi uzantilarin ayni olmasidiir

@app.get("/courses/byid/{course_id}")
async def get_course_by_id(course_id: int):
    for id in courses_db:
        if id.get('id') == course_id:
            return id



#query example
@app.get("/courses/")
async def get_category_by_query(category:str):
    courses_to_return=[]
    #tek bir deger dondurmayecegim icin dizi olusturdum
    for course in courses_db:
        if course.get('category').casefold()==category.casefold():
            courses_to_return.append(course)
    return courses_to_return
#http://127.0.0.1:8000/courses/?category=cloud soru isareti oldugu icin bunun bir query oldugunu anliyoruz

#path and query filtreleme yaptik
@app.get("/courses/{course_instructor}/")
async def get_instructor_category_by_query(course_instructor:str , category:str):
    courses_to_return=[]
    for course in courses_db:
        if (course.get('instructor').casefold()==course_instructor.casefold()
                and course.get('category').casefold() == category.casefold()):
            courses_to_return.append(course)
    return courses_to_return
