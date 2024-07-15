from fastapi import APIRouter, HTTPException
from app.models.predicitons import PredictionInput, PredictionOutput, ModelMetrics
import pandas as pd
import numpy as np
import sqlite3 as sq
import app.database as db
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

router = APIRouter()

# Load data
database = db.Database()
df = database.get_data("athletes")

# Global variables to store the model and scaler
model = None
feature_columns = ['Age', 'Height', 'Weight']

@router.post("/predictions/train", response_model=dict, tags=["Predictions"])
async def train_model():
    global model, feature_columns
    
    # Prepare the data
    X = df[feature_columns + ['Sex', 'Sport']]
    y = df['Medal'].fillna('No Medal')
    
    # Encode categorical variables
    X = pd.get_dummies(X, columns=['Sex', 'Sport'])
    
    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Create and train the model
    model = Pipeline([
        ('scaler', StandardScaler()),
        ('classifier', RandomForestClassifier(n_estimators=100, random_state=42))
    ])
    
    model.fit(X_train, y_train)
    
    # Calculate metrics
    y_pred = model.predict(X_test)
    metrics = ModelMetrics(
        accuracy=accuracy_score(y_test, y_pred),
        precision=precision_score(y_test, y_pred, average='weighted'),
        recall=recall_score(y_test, y_pred, average='weighted'),
        f1_score=f1_score(y_test, y_pred, average='weighted')
    )
    
    return {"message": "Model trained successfully", "metrics": metrics}

@router.post("/predictions/predict", response_model=PredictionOutput, tags=["Predictions"])
async def predict_medal(input_data: PredictionInput):
    if model is None:
        raise HTTPException(status_code=400, detail="Model not trained. Please train the model first.")
    
    # Prepare input data
    input_df = pd.DataFrame([input_data.dict()])
    input_df = pd.get_dummies(input_df, columns=['Sex', 'Sport'])
    
    # Ensure all columns from training are present
    for col in model.named_steps['classifier'].feature_names_in_:
        if col not in input_df.columns:
            input_df[col] = 0
    
    # Reorder columns to match training data
    input_df = input_df[model.named_steps['classifier'].feature_names_in_]
    
    # Make prediction
    prediction = model.predict(input_df)[0]
    probability = max(model.predict_proba(input_df)[0])
    
    return PredictionOutput(predicted_medal=prediction, probability=probability)

@router.get("/predictions/top_features", tags=["Predictions"])
async def get_top_features():
    if model is None:
        raise HTTPException(status_code=400, detail="Model not trained. Please train the model first.")
    
    feature_importances = model.named_steps['classifier'].feature_importances_
    feature_names = model.named_steps['classifier'].feature_names_in_
    
    top_features = sorted(zip(feature_names, feature_importances), key=lambda x: x[1], reverse=True)[:10]
    
    return {"top_features": [{"feature": name, "importance": float(importance)} for name, importance in top_features]}

@router.get("/predictions/medal_distribution", tags=["Predictions"])
async def get_medal_distribution():
    medal_counts = df['Medal'].value_counts(dropna=False)
    total = medal_counts.sum()
    
    distribution = {
        medal: {
            "count": int(count),
            "percentage": float(count / total * 100)
        }
        for medal, count in medal_counts.items()
    }
    
    return {"medal_distribution": distribution}