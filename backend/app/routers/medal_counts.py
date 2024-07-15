from fastapi import APIRouter
from typing import List
from app.models.general import MedalCount
import pandas as pd
import numpy as np
import sqlite3 as sq

router = APIRouter()

# Load data
conn = sq.connect("database/olympics.db")
df = pd.read_sql("SELECT * FROM athletes", conn)

@router.get("/medal_counts/{sport}", response_model=List[MedalCount], tags=["Medal Counts"])
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

@router.get("/medal_counts", response_model=List[MedalCount], tags=["Medal Counts"])
async def get_medal_counts_by_country_and_sport(country: str, sport: str):
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