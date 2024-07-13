import uvicorn
import pandas as pd
import numpy as np
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI()

# Load data from CSV
df = pd.read_csv("data/athlete_events.csv")

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

@app.get("/athletes", response_model=List[OlympicAthlete])
async def get_athletes(skip: int = 0, limit: int = 10):
    athletes = df.iloc[skip:skip+limit].replace({np.nan: None}).to_dict(orient="records")
    return [OlympicAthlete(**athlete) for athlete in athletes]

@app.get("/athletes/{athlete_id}", response_model=OlympicAthlete)
async def get_athlete(athlete_id: int):
    athlete = df[df['ID'] == athlete_id]
    if athlete.empty:
        raise HTTPException(status_code=404, detail="Athlete not found")
    athlete_dict = athlete.replace({np.nan: None}).to_dict(orient="records")[0]
    return OlympicAthlete(**athlete_dict)

@app.get("/athletes/search")
async def search_athletes(name: Optional[str] = None, sport: Optional[str] = None):
    result = df
    if name:
        result = result[result['Name'].str.contains(name, case=False)]
    if sport:
        result = result[result['Sport'].str.contains(sport, case=False)]
    athletes = result.replace({np.nan: None}).to_dict(orient="records")
    return [OlympicAthlete(**athlete) for athlete in athletes]

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)