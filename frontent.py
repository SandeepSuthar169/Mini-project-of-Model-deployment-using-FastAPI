import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/predict"  # Replace with server IP if not localhost

st.title("Heart Disease Category Predictor")
st.markdown("Please fill in your health details below:")

with st.form("heart_form"):
    Age = st.number_input("Age", min_value=1, max_value=119, value=30)
    Sex = st.selectbox("Sex", options=["M", "F"])
    ChestPainType = st.selectbox("Chest Pain Type", options=["TA", "ATA", "NAP", "ASY"])  # example categories
    RestingBP = st.number_input("Resting Blood Pressure", min_value=0, value=120)
    Cholesterol = st.number_input("Cholesterol", min_value=0, value=200)
    FastingBS = st.selectbox("Fasting Blood Sugar > 120 mg/dl", options=[0, 1])
    RestingECG = st.selectbox("Resting ECG", options=["Normal", "ST", "LVH"])
    MaxHR = st.number_input("Max Heart Rate", min_value=0, value=150)
    ExerciseAngina = st.selectbox("Exercise-Induced Angina", options=["Y", "N"])
    Oldpeak = st.number_input("Oldpeak", min_value=0.0, step=0.1, value=1.0)
    ST_Slope = st.selectbox("ST Slope", options=["Up", "Flat", "Down"])

    submitted = st.form_submit_button("Predict Health Details Category")

if submitted:
    input_data = {
        "Age": Age,
        "Sex": Sex,
        "ChestPainType": ChestPainType,
        "RestingBP": RestingBP,
        "Cholesterol": Cholesterol,
        "FastingBS": FastingBS,
        "RestingECG": RestingECG,
        "MaxHR": MaxHR,
        "ExerciseAngina": ExerciseAngina,
        "Oldpeak": Oldpeak,
        "ST_Slope": ST_Slope
    }

    try:
        response = requests.post(API_URL, json=input_data)

        if response.status_code == 200:
            result = response.json()
            st.success(f"Predicted Category: **{result['predicted_category']}**")
        else:
            st.error(f"API Error: {response.status_code} - {response.text}")

    except requests.exceptions.ConnectionError:
        st.error("Failed to connect to the FastAPI server. Is it running?")
    except requests.exceptions.JSONDecodeError:
        st.error("Received non-JSON response from the server.")
        st.text(response.text)
