from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from app.models.general import OlympicAthlete
import pandas as pd
import numpy as np
import app.database as db

router = APIRouter()

# Load data
database = db.Database()
df = database.get_data("athletes")

@router.get("/athletes", response_model=List[OlympicAthlete], tags=["Athletes"])
async def get_athletes(skip: int = 0, limit: int = 10):
    athletes = df.iloc[skip:skip+limit].replace({np.nan: None}).to_dict(orient="records")
    return [OlympicAthlete(**athlete) for athlete in athletes]

@router.get("/athletes/search", response_model=List[OlympicAthlete], tags=["Athletes"])
async def search_athletes(
    name: Optional[str] = Query(None, description="Name of the athlete"),
    sport: Optional[str] = Query(None, description="Sport of the athlete"),
    team: Optional[str] = Query(None, description="Team of the athlete"),
    year: Optional[int] = Query(None, description="Year of the Olympic event"),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(10, ge=1, le=100, description="Number of records to return")
):
    result = df

    if name:
        result = result[result['Name'].str.contains(name, case=False, na=False)]
    if sport:
        result = result[result['Sport'].str.contains(sport, case=False, na=False)]
    if team:
        result = result[result['Team'].str.contains(team, case=False, na=False)]
    if year:
        result = result[result['Year'] == year]

    result = result.iloc[skip:skip+limit]

    athletes = result.replace({np.nan: None}).to_dict(orient="records")
    return [OlympicAthlete(**athlete) for athlete in athletes]

@router.get("/athletes/{athlete_id}", response_model=OlympicAthlete, tags=["Athletes"])
async def get_athlete(athlete_id: int):
    athlete = df[df['ID'] == athlete_id]
    if athlete.empty:
        raise HTTPException(status_code=404, detail="Athlete not found")
    athlete_dict = athlete.replace({np.nan: None}).to_dict(orient="records")[0]
    return OlympicAthlete(**athlete_dict)