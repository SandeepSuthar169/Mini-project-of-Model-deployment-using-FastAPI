import streamlit as st
import requests

API_URL = 'http://34.226.152.222:8000/predict'


st.title('Heart Disease Category Predictor')
st.markdown("Enter your details below:")

Age = st.number_input('Age', min_value=1, max_value=119, value=30)
Sex = st.selectbox('Sex', options=["M", "F"])
ChestPainType  = st.number_input('ChestPainType', min_value=0, value=120)
RestingBP = st.number_input('RestingBP', min_value=0, value=200)
Cholesterol = st.number_input('Cholesterol',min_value=0, value= 200)
FastingBS = st.selectbox('FastingBS', options=[0, 1])
RestingECG = st.selectbox('RestingECG', options=['Normal', 'ST', "LVH"])
MaxHR  = st.number_input('MaxHR ',min_value=0, value=150)
ExerciseAngina  = st.selectbox('ExerciseAngina', options=['Y', 'N'])
Oldpeak = st.number_input('Oldpeak', min_value=0.0, step=0.1, value=1.0)
ST_Slope = st.selectbox('ST_Slope', options=['Up', 'Flat', 'Down'])

if st.button("Predict Heart Disease Category"):
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
        response = requests.post(API_URL, json = input_data)
        result = response.json

        if response.status_code == 200 and 'response' in result:
            prediction  = result['response']
            st.success(f"Predict Heart Disease Category: **{prediction['predicted_category']}**")
            st.write('Confidance:', prediction['confidance'])
            st.write('class Probavilities')
            st.json(prediction['class_probabilities'])

        else:
            st.error(f"API Error: {response.status_code}")
            st.write(result)

    except requests.exceptions.ConnectionError:
        st.error('coluld not connect to the FastAPI server')        
