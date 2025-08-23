import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")

st.set_page_config(page_title="🌤 Weather App", page_icon="☁️", layout="centered")

st.title("🌍 Free Weather App")
city = st.text_input("Enter city name:", "London")

def get_openweather(city):
    """Fetch weather from OpenWeather API"""
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    try:
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            data = r.json()
            return {
                "source": "OpenWeather",
                "city": data["name"],
                "country": data["sys"]["country"],
                "temperature": data["main"]["temp"],
                "feels_like": data["main"]["feels_like"],
                "humidity": data["main"]["humidity"],
                "weather": data["weather"][0]["description"].title()
            }
        else:
            return None
    except Exception as e:
        return None

def get_wttr(city):
    """Fetch weather from wttr.in (no API key needed)"""
    url = f"https://wttr.in/{city}?format=j1"
    try:
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            data = r.json()
            current = data["current_condition"][0]
            return {
                "source": "wttr.in",
                "city": city.title(),
                "country": "N/A",
                "temperature": float(current["temp_C"]),
                "feels_like": float(current["FeelsLikeC"]),
                "humidity": current["humidity"],
                "weather": current["weatherDesc"][0]["value"]
            }
        else:
            return None
    except Exception:
        return None

if st.button("Get Weather"):
    result = None
    if API_KEY:
        result = get_openweather(city)
    if not result:
        result = get_wttr(city)

    if result:
        st.success(f"✅ Weather data from {result['source']}")
        st.metric("🌡 Temperature (°C)", result["temperature"], delta=None)
        st.metric("🤔 Feels Like (°C)", result["feels_like"])
        st.metric("💧 Humidity (%)", result["humidity"])
        st.write(f"**Condition:** {result['weather']}")
    else:
        st.error("❌ Could not fetch weather data. Please try again.")