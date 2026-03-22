import streamlit as st
import requests
import pandas as pd
import pickle

# -------------------------
# Load ML model
# -------------------------
model = pickle.load(open("crop_model.pkl", "rb"))

# -------------------------
# Weather API key
# -------------------------
API_KEY = "a7d857537e2333177054d889e3e1513a"


# -------------------------
# Function to fetch weather
# -------------------------
def get_weather(city):

    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

    response = requests.get(url)
    data = response.json()

    temperature = data["main"]["temp"]
    humidity = data["main"]["humidity"]
    rainfall = data.get("rain", {}).get("1h", 0)

    return temperature, humidity, rainfall


# -------------------------
# Streamlit UI
# -------------------------

st.title("🌱 Smart Crop Recommendation System")

st.write("Enter soil values and location to get crop recommendation")

# -------------------------
# User Inputs
# -------------------------

city = st.text_input("Enter City")

N = st.number_input("Nitrogen (N)", min_value=0)
P = st.number_input("Phosphorus (P)", min_value=0)
K = st.number_input("Potassium (K)", min_value=0)
ph = st.number_input("Soil pH", min_value=0.0, max_value=14.0)


# -------------------------
# Prediction Button
# -------------------------

if st.button("Predict Crop"):

    try:

        temperature, humidity, rainfall = get_weather(city)

        input_data = pd.DataFrame(
            [[N, P, K, temperature, humidity, ph, rainfall]],
            columns=["N","P","K","temperature","humidity","ph","rainfall"]
        )

        prediction = model.predict(input_data)

        st.subheader("🌤 Weather Information")
        st.write("Temperature:", temperature, "°C")
        st.write("Humidity:", humidity, "%")
        st.write("Rainfall:", rainfall, "mm")

        st.subheader("🌾 Recommended Crop")
        st.success(prediction[0])

    except:
        st.error("Unable to fetch weather data. Please check city name.")