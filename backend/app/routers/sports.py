from fastapi import APIRouter
from app.models.general import SportsbySeasonResponse
import pandas as pd
import sqlite3 as sq

router = APIRouter()

# Load data
conn = sq.connect("database/olympics.db")
df = pd.read_sql("SELECT * FROM athletes", conn)

@router.get("/sports/sports_by_season", response_model=SportsbySeasonResponse, tags=["Sports"])
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