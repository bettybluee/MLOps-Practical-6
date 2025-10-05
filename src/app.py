import streamlit as st
import requests

st.title("My Text Classifier")

txt = st.text_area("Enter text:")

if st.button("Predict"):
    r = requests.post("http://localhost:8000/predict", json={"text": txt})
    st.write("Prediction:", r.json()["prediction"])