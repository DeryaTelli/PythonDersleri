from sqlalchemy.orm import Session
from sqlalchemy import select, func, and_
from datetime import datetime, date
from app.domain.location import LocationPoint
from app.domain.user import User, Role

class LocationRepository:
    def __init__(self, db: Session):
        self.db = db

    def save_point(self, user_id: int, lat: float, lon: float, when: datetime | None = None) -> LocationPoint:
        when = when or datetime.utcnow()
        obj = LocationPoint(user_id=user_id, lat=lat, lon=lon, created_at=when, day=when.date())
        self.db.add(obj); self.db.commit(); self.db.refresh(obj)
        return obj

    def list_points_for_day(self, user_id: int, day: date) -> list[LocationPoint]:
        stmt = select(LocationPoint).where(
            and_(LocationPoint.user_id == user_id, LocationPoint.day == day)
        ).order_by(LocationPoint.created_at.asc())
        return list(self.db.scalars(stmt))

    def last_point_for_user(self, user_id: int) -> LocationPoint | None:
        stmt = select(LocationPoint).where(LocationPoint.user_id == user_id)\
                                    .order_by(LocationPoint.created_at.desc()).limit(1)
        return self.db.scalar(stmt)

    def last_points_for_all_users(self) -> list[tuple[User, LocationPoint]]:
        # aktif tüm user'lar için son nokta
        users = list(self.db.scalars(select(User).where(User.role == Role.user, User.is_active == True)))
        out = []
        for u in users:
            last = self.last_point_for_user(u.id)
            if last: out.append((u, last))
        return out
