from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Literal
from fastapi.responses import JSONResponse
import pandas as pd
import pickle

# Load model
with open("notebook/model.pkl", "rb") as file:
    model = pickle.load(file)

app = FastAPI(title="Heart Disease Prediction API")

# Define input data schema
class HeartData(BaseModel):
    Age: int = Field(..., gt=0, lt=120, description="Age of the user")
    Sex: Literal["M", "F"]
    ChestPainType: Literal[1, 2, 3, 4]  # Encoded already
    RestingBP: int
    Cholesterol: int
    FastingBS: Literal[0, 1]
    RestingECG: Literal[1, 2, 3]  # Encoded already
    MaxHR: int
    ExerciseAngina: Literal["Y", "N"]
    Oldpeak: float
    ST_Slope: Literal[1, 2, 3]  # Encoded already

@app.post("/predict")
def predict(data: HeartData):
    # Convert input to DataFrame
    input_df = pd.DataFrame([data.dict()])

    # Make prediction
    try:
        prediction = model.predict(input_df)[0]
        return JSONResponse(status_code=200, content={"predicted_category": int(prediction)})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

