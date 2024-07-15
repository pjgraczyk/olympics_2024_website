from pydantic import BaseModel

class PredictionInput(BaseModel):
    Age: float
    Height: float
    Weight: float
    Sex: str
    Sport: str

class PredictionOutput(BaseModel):
    predicted_medal: str
    probability: float

class ModelMetrics(BaseModel):
    accuracy: float
    precision: float
    recall: float
    f1_score: float