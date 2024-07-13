import uvicorn
import pandas as pd
import numpy as np
import sqlite3 as sq
from typing import List, Optional
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Load data from CSV
conn = sq.connect("database/olympics.db")
df = pd.read_sql("SELECT * FROM athletes", conn)

class OlympicAthlete(BaseModel):
    ID: str
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

class CountryPredictionRequest(BaseModel):
    Year: int
    NOC: str
    AthleteCount: int
    AverageAge: float
    AverageHeight: float
    AverageWeight: float

class CountryPredictionResponse(BaseModel):
    NOC: str
    PredictedMedals: int

class SportsbySeasonResponse(BaseModel):
    Summer: List[str]
    Winter: List[str]
    
class MedalCount(BaseModel):
    country: str
    gold: int
    silver: int
    bronze: int
    total: int

@app.get("/medal_counts/{sport}", response_model=List[MedalCount])
async def get_medal_counts(sport: str):
    sport_df = df[df['Sport'] == sport]
    medal_counts = sport_df[sport_df['Medal'].notna()].groupby('NOC')['Medal'].value_counts().unstack(fill_value=0)
    
    if 'Gold' not in medal_counts.columns:
        medal_counts['Gold'] = 0
    if 'Silver' not in medal_counts.columns:
        medal_counts['Silver'] = 0
    if 'Bronze' not in medal_counts.columns:
        medal_counts['Bronze'] = 0
    
    medal_counts['Total'] = medal_counts['Gold'] + medal_counts['Silver'] + medal_counts['Bronze']
    medal_counts = medal_counts.sort_values('Total', ascending=False).reset_index()
    
    return [
        MedalCount(
            country=row['NOC'],
            gold=row['Gold'],
            silver=row['Silver'],
            bronze=row['Bronze'],
            total=row['Total']
        )
        for _, row in medal_counts.iterrows()
    ]

@app.get("/medal_counts/?country={country}?sport={sport}", response_model=List[MedalCount])
async def get_medal_counts(country: str, sport: str):
    sport_df = df[(df['Sport'] == sport) & (df['NOC'] == country)]
    medal_counts = sport_df[sport_df['Medal'].notna()].groupby('NOC')['Medal'].value_counts().unstack(fill_value=0)
    
    if 'Gold' not in medal_counts.columns:
        medal_counts['Gold'] = 0
    if 'Silver' not in medal_counts.columns:
        medal_counts['Silver'] = 0
    if 'Bronze' not in medal_counts.columns:
        medal_counts['Bronze'] = 0
    
    medal_counts['Total'] = medal_counts['Gold'] + medal_counts['Silver'] + medal_counts['Bronze']
    medal_counts = medal_counts.sort_values('Total', ascending=False).reset_index()
    
    return [
        MedalCount(
            country=row['NOC'],
            gold=row['Gold'],
            silver=row['Silver'],
            bronze=row['Bronze'],
            total=row['Total']
        )
        for _, row in medal_counts.iterrows()
    ]

@app.get("/athletes", response_model=List[OlympicAthlete])
async def get_athletes(skip: int = 0, limit: int = 10):
    athletes = df.iloc[skip:skip+limit].replace({np.nan: None}).to_dict(orient="records")
    return [OlympicAthlete(**athlete) for athlete in athletes]

@app.get("/athletes/search", response_model=List[OlympicAthlete])
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

    total_count = len(result)
    result = result.iloc[skip:skip+limit]

    athletes = result.replace({np.nan: None}).to_dict(orient="records")
    return [OlympicAthlete(**athlete) for athlete in athletes]

@app.get("/athletes/{athlete_id}", response_model=OlympicAthlete)
async def get_athlete(athlete_id: int):
    athlete = df[df['ID'] == athlete_id]
    if athlete.empty:
        raise HTTPException(status_code=404, detail="Athlete not found")
    athlete_dict = athlete.replace({np.nan: None}).to_dict(orient="records")[0]
    return OlympicAthlete(**athlete_dict)

@app.get("/sports_by_season", response_model=SportsbySeasonResponse)
async def get_sports_by_season():
    # Group by Season and Sport, then get unique combinations
    sports_by_season = df.groupby('Season')['Sport'].unique().to_dict()
    
    # Convert numpy arrays to lists and sort
    for season in sports_by_season:
        sports_by_season[season] = sorted(sports_by_season[season].tolist())
    
    # Ensure both Summer and Winter keys exist
    if 'Summer' not in sports_by_season:
        sports_by_season['Summer'] = []
    if 'Winter' not in sports_by_season:
        sports_by_season['Winter'] = []
    
    return SportsbySeasonResponse(**sports_by_season)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)