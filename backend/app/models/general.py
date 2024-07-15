from pydantic import BaseModel
from typing import Optional, List

class OlympicAthlete(BaseModel):
    ID: int
    Name: str
    Sex: str
    Age: Optional[float] = None
    Height: Optional[float] = None
    Weight: Optional[float] = None
    Team: str
    NOC: str
    Games: str
    Year: int
    Season: str
    City: str
    Sport: str
    Event: str
    Medal: Optional[str] = None

    class Config:
        from_attributes = True

class MedalCount(BaseModel):
    country: str
    gold: int
    silver: int
    bronze: int
    total: int

class SportsbySeasonResponse(BaseModel):
    Summer: List[str]
    Winter: List[str]