from pydantic import BaseModel, Field
from datetime import datetime, date

class LocationIn(BaseModel):
    lat: float = Field(ge=-90, le=90)
    lon: float = Field(ge=-180, le=180)

class LocationOut(BaseModel):
    user_id: int
    lat: float
    lon: float
    created_at: datetime

class LastLocation(BaseModel):
    user_id: int
    first_name: str
    last_name: str
    lat: float
    lon: float
    created_at: datetime

class DayQuery(BaseModel):
    day: date
