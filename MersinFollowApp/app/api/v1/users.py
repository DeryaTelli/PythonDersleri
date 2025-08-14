from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api.deps import get_db, require_admin_key ,get_current_user
from app.schemas.user import UserCreate, UserOut, UserLogin, TokenOut
from app.services.user_service import UserService
from app.domain.user import User as UserEntity

router = APIRouter(prefix="/users", tags=["users"])
#bu router altindaki tum endpointlerin urlsi /users ile baslayacak

@router.post("/login", response_model=TokenOut)
def login(payload: UserLogin, db: Session = Depends(get_db)):
    svc = UserService(db)
    try:
        token = svc.authenticate(payload.email, payload.password)
        return {"access_token": token, "token_type": "bearer"}
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))

# ADMIN-ONLY: kullanıcı oluşturma
@router.post("/admin/users", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def admin_create_user(
    payload: UserCreate,
    db: Session = Depends(get_db),
    _ok: bool = Depends(require_admin_key),
):
    svc = UserService(db)
    try:
        user = svc.register_user(payload)
        return user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/me", response_model=UserOut)
def me(current_user: UserEntity = Depends(get_current_user)):
    return current_user