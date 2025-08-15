from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api.deps import get_db, require_admin_key ,get_current_user, require_admin_jwt
from app.schemas.user import UserCreate, UserOut, UserLogin, TokenOut ,Role as RoleSchema
from app.services.user_service import UserService
from app.domain.user import User as UserEntity
from typing import List
from app.repositories.user_repo import UserRepository
from app.domain.user import Role as RoleDomain

router = APIRouter(prefix="/users", tags=["users"])
#bu router altindaki tum endpointlerin urlsi /users ile baslayacak

@router.get("/admin/users", response_model=List[UserOut])
def admin_list_users(
    role: RoleSchema | None = None,   # ?role=user gibi
    db: Session = Depends(get_db),
    _admin = Depends(require_admin_jwt),
):
    repo = UserRepository(db)
    domain_role = RoleDomain(role.value) if role else None
    return repo.list_by_role(domain_role)

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
