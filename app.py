from fastapi import FastAPI
from pydantic import BaseModel, Field, computed_field
from fastapi.responses import JSONResponse
from typing import Literal, Annotated
import pickle
import pandas as pd
import numpy as np


with open("notebook/model.pkl", "rb") as file:
    model = pickle.load(file)

app = FastAPI(title="Heart Disease Prediction API")


class HeartData(BaseModel):
    age: Annotated[int, Field(..., gt=0, lt=120, description='age of the user')]
    Sex: Annotated[object, Field(..., description='gender of the user')]
    ChestPainType: Annotated[object, Field(..., description='chest pain of the userof different level pain')]
    RestingBP: Annotated[int, Field(..., description='pressure of blood of user in mm Hg')]
    Cholesterol: Annotated[int, Field(..., description='Total amound of cholesterol in person blood (HDL), (LDL)')]
    FastingBS: Annotated[int, Field(..., description= '0 or 1')]
    RestingECG: Annotated[object, Field(..., description='Resting Electrocardiogram Results, normal, ST, LVH')]
    MaxHR: Annotated[int, Field(...,description= 'Maximum Heart Rate')]
    ExerciseAngina: Annotated[object, Field(..., description='the patient experienced angina (chest pain) during exercise')]
    Oldpeak: Annotated[float, Field(..., description='Millimeters (mm) of ST segment depression')]
    ST_Slope: Annotated[object, Field(..., description='Slope of the ST Segment')]


@app.post("/predict")
def predict(data: HeartData):
    
    input_data = {
        "Sex": [data.Sex],
        "ChestPainType": [data.ChestPainType],
        "RestingBP": [data.RestingBP],
        "Cholesterol": [data.Cholesterol],
        "FastingBS": [data.FastingBS],
        "RestingECG": [data.RestingECG],
        "MaxHR": [data.MaxHR],
        "ExerciseAngina": [data.ExerciseAngina],
        "Oldpeak": [data.Oldpeak],
        "ST_Slope": [data.ST_Slope],
        "Age": [data.Age],
    }

    import pandas as pd
    df = pd.DataFrame(input_data)

    # Predict
    prediction = model.predict(df)[0]
    return {"prediction": int(prediction)}
