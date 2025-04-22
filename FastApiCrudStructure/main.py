from fastapi import FastAPI, Body,Path , Query ,HTTPException
#yukaridakiler kullanacagim kutuphaneler
from typing import Optional
from pydantic import BaseModel , Field
from starlette import status

#http status kodlarin ne anlama geldiklerine bak onlara gore islem gerceklestirecegiz

app=FastAPI()

class Course:
    id:int
    title:str
    instructor:str
    rating:int
    published_date:int

    def __init__(self, id:int , title:str,instructor:str,rating:int,published_date:int):
        self.id=id
        self.title=title
        self.instructor=instructor
        self.rating=rating
        self.published_date=published_date

class CourseRequest(BaseModel):
    id: Optional[int]=Field(description="The id of the course, optional",default=None)
    title: str =Field(min_length=1 , max_length=100 )
    instructor: str = Field(min_length=3)
    rating: int=Field(gt=0,lt=6)
    published_date:int=Field(gte=1900,lte=2100)

    model_config={
        #json dosyasinin nasil olmasini istiyorsam burada o sekilde belirtiyorum
        "json_schema_extra":{
            "example":{
                "title" : "My Course",
                "instructor": "<NAME>",
                "rating":5,
                "published_date":2020
            }
        }
    }

courses_db=[
    Course(1,'Python', 'Derya',5,2029),
    Course(2, 'Kotlin', 'Baris', 5, 2026),
    Course(3, 'Java', 'Asli', 5, 2023),
    Course(4, 'Jenkis', 'Zilan', 2, 2030),
    Course(5, 'C', 'Ece', 1, 2036),
    Course(6, 'Machine Learning', 'Derya', 3, 2039),
]

#status kod belirtiyoruz import ettigimiz kutuphaneden geliyor
@app.get("/courses",status_code=status.HTTP_200_OK)
async def get_all_courses():
    return courses_db

@app.get("/courses/{course_id}", status_code=status.HTTP_200_OK)
async def get_course(course_id:int=Path(gt=0)):
    #gt=0 demek 0 dan buyuk demek lt ise verilen degerden kucuk demek
    for course in courses_db:
        if course.id ==course_id:
            return course
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not fount")
    #hata aldiginda olusacak durumun http kodu ve onun icin gostermesini istedigmiz detay mesaji


@app.get("/courses/", status_code=status.HTTP_200_OK)
async def get_courses_by_rating(course_rating: int=Query(gt=0 ,lt=6)):
    courses_to_return=[]
    for course in courses_db:
        if course.rating==course_rating:
            courses_to_return.append(course)
    return courses_to_return

@app.get("/courses/publish/", status_code=status.HTTP_200_OK)
async def get_courses_by_publish_date(publish_date:int =Query(gt=2005 , lt=2040)):
    courses_to_return=[]
    for course in courses_db:
        if course.published_date==publish_date:
            courses_to_return.append(course)
    return courses_to_return

#ayni pathler oldugu icin hata verecek birinde rating digerinde publish_date gore almama ragmen
#pathler birbiriyle ayni sonra

@app.post("create_course", status_code=status.HTTP_201_CREATED)
async def create_course(course_request :CourseRequest):
    new_course=Course(**course_request.model_dump() )
    courses_db.append(find_course_id(new_course))

#-1 degeri son idyi verir
def find_course_id(course: Course):
    course.id = 1 if len(courses_db)==0 else courses_db[-1].id+1
    return course

@app.put("/courses/update_course",status.HTTP_204_NO_CONTENT)
async  def update_course(course_request: CourseRequest):
    course_updated=False
    for i in range(len(courses_db)):
        #indexine gore bulup degisim yapmak icin bu sekilde for dongusune koyduk
        if courses_db[i].id==course_request.id:
            courses_db[i]=course_request
            course_updated=True
        if not course_updated:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")


@app.delete("/courses/delete/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_course(course_id: int=Path(gt=0)):
    course_deleted=False
    for i in range(len(courses_db)):
        if courses_db[i].id==course_id:
            courses_db.pop(i)
            course_deleted=True
            break
        if not course_deleted:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")