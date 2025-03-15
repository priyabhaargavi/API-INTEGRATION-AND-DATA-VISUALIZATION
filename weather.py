import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

API_KEY = "52ee9d355c3cf46c2b317195b94dd60b"

def fetch_weather_data(city):
    API_URL = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(API_URL)
    if response.status_code == 200:
        data = response.json()
        return pd.DataFrame({
            "time": pd.to_datetime([item["dt_txt"] for item in data["list"]]),
            "temperature": [item["main"]["temp"] for item in data["list"]],
            "humidity": [item["main"]["humidity"] for item in data["list"]],
            "wind_speed": [item["wind"]["speed"] for item in data["list"]]
        })
    else:
        st.error("Failed to fetch data. Please check your API key or city name.")
        return None

st.set_page_config(page_title="Weather Dashboard", layout="wide")

st.sidebar.title("Select City")
cities = ["London", "New York", "Tokyo", "Sydney", "Paris", "Mumbai"]
city = st.sidebar.selectbox("Choose a city:", cities)

df = fetch_weather_data(city)

if df is not None:
    sns.set_style("darkgrid")

    st.title(f"Weather Dashboard - {city}")

    st.subheader("Temperature Over Time")
    fig, ax = plt.subplots(figsize=(10, 4))
    sns.lineplot(data=df, x="time", y="temperature", ax=ax, color="red")
    ax.set_ylabel("Temperature (°C)")
    st.pyplot(fig)

    st.subheader("Humidity Over Time")
    fig, ax = plt.subplots(figsize=(10, 4))
    sns.lineplot(data=df, x="time", y="humidity", ax=ax, color="blue")
    ax.set_ylabel("Humidity (%)")
    st.pyplot(fig)

    st.subheader("Wind Speed Over Time")
    fig, ax = plt.subplots(figsize=(10, 4))
    sns.lineplot(data=df, x="time", y="wind_speed", ax=ax, color="green")
    ax.set_ylabel("Wind Speed (m/s)")
    st.pyplot(fig)

    st.subheader("Raw Data")
    st.dataframe(df)