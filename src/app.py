import streamlit as st
import requests

st.title("My Text Classifier")

# Sidebar example input
example_input = st.sidebar.selectbox(
    "Try an example input",
    ["I love this!", "This is terrible.", "Not sure about this."]
)

# Main text area, defaulting to sidebar selection
user_input = st.text_area("Or enter your own text:", value=example_input)

if st.button("Predict"):
    try:
        # Send request to FastAPI server
        response = requests.post("http://localhost:8000/predict", json={"text": user_input})
        st.write("Prediction:", response.json()["prediction"])
    except:
        st.write("⚠️ Make sure the FastAPI server is running.")


