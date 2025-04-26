from fastapi import APIRouter
#router mantigi
# bir klasor olusturup end pointerli kapsayan tum islemleri bir dosya icinde toplar
# icinde bir tane app oluyor onlari yolluyor farkli end pointler tek bir app icerisinde yer alabiliyor


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)

@router.get("/get_user")
async def get_user():
    return "Hello World!"
