import uvicorn
import sqlite3
import pandas as pd
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import athletes, medal_counts, sports, predictions

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(athletes.router)
app.include_router(medal_counts.router)
app.include_router(sports.router)
app.include_router(predictions.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
