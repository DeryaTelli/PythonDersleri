from sqlalchemy.orm import Session
from app.domain.user import User, Gender as GenderDomain, Role as RoleDomain
from app.schemas.user import UserCreate
from app.core.security import hash_password, verify_password, create_access_token
from app.repositories.user_repo import UserRepository

class UserService:
    def __init__(self, db: Session):
        self.repo = UserRepository(db)

    def register_user(self, data: UserCreate) -> User:
        if self.repo.get_by_email(data.email):
            raise ValueError("Email already in use.")
        entity = User(
            first_name=data.first_name,
            last_name=data.last_name,
            email=data.email,
            password_hash=hash_password(data.password),
            gender=GenderDomain(data.gender),
            role=RoleDomain(data.role),
            server_token=data.server_token,  # “kendim gireceğim” derseniz buradan verilir
        )
        return self.repo.create(entity)

    def authenticate(self, email: str, password: str) -> str:
        user = self.repo.get_by_email(email)
        if not user or not verify_password(password, user.password_hash) or not user.is_active:
            raise ValueError("Invalid credentials.")
        # Flutter bu JWT ile giriş yapacak
        return create_access_token(str(user.id), extra={"email": user.email, "role": user.role.value} )
