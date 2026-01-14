import streamlit as st
import requests

# ---------------- CONFIG ----------------
st.set_page_config(
    page_title="CongestiQ AI",
    page_icon="🚦",
    layout="centered"
)

API_KEY = st.secrets["OPENWEATHER_API_KEY"]


# ---------------- HEADER ----------------
st.markdown("<h1 style='text-align:center;'>🚦 CongestiQ AI</h1>", unsafe_allow_html=True)
st.markdown(
    "<p style='text-align:center;'>AI-Powered Real-Time Traffic Congestion & Risk Intelligence</p>",
    unsafe_allow_html=True
)

st.info(
    "CongestiQ AI automatically fetches real-time weather and climate data "
    "and intelligently estimates traffic congestion risk for smart cities."
)

st.divider()

# ---------------- LOCATION INPUT ----------------
st.subheader("📍 Location")
city = st.text_input("Enter City Name", "Chennai")

# ---------------- FETCH REAL-TIME WEATHER ----------------
@st.cache_data(ttl=600)
def fetch_weather(city):
    url = (
        f"https://api.openweathermap.org/data/2.5/weather?"
        f"q={city}&appid={API_KEY}&units=metric"
    )
    response = requests.get(url)
    return response.json()

weather_data = None
if city:
    weather_data = fetch_weather(city)

if weather_data and weather_data.get("cod") != 200:
    st.error("City not found or API error.")
    st.stop()

# ---------------- TRAFFIC INPUT ----------------
st.subheader("🚗 Traffic Conditions")
traffic_density = st.slider("Traffic Density (%)", 0, 100, 50)
avg_speed = st.slider("Average Speed (km/h)", 0, 120, 40)
peak_hour = st.selectbox("Peak Hour", ["No", "Yes"])
accident = st.selectbox("Recent Accident", ["No", "Yes"])
construction = st.selectbox("Road Construction", ["No", "Yes"])

# ---------------- SAFETY INPUT ----------------
st.subheader("🛑 Safety Compliance")
helmet_usage = st.slider("Helmet Usage (%)", 0, 100, 70)
seatbelt_usage = st.slider("Seatbelt Usage (%)", 0, 100, 80)
speeding = st.selectbox("Speeding Observed", ["No", "Yes"])

st.divider()

# ---------------- EXTRACT WEATHER DATA ----------------
temp = weather_data["main"]["temp"]
humidity = weather_data["main"]["humidity"]
wind_speed = weather_data["wind"]["speed"]
visibility = weather_data.get("visibility", 1000)
weather_condition = weather_data["weather"][0]["main"]

# ---------------- AI RISK ENGINE ----------------
traffic_risk = 0
weather_risk = 0
safety_risk = 0

# ---- Traffic Risk ----
traffic_risk += traffic_density * 0.4
traffic_risk += max(0, 60 - avg_speed) * 0.35
if peak_hour == "Yes":
    traffic_risk += 10
if accident == "Yes":
    traffic_risk += 20
if construction == "Yes":
    traffic_risk += 15

# ---- Weather Risk ----
weather_weights = {
    "Clear": 0,
    "Rain": 15,
    "Drizzle": 10,
    "Thunderstorm": 25,
    "Fog": 20,
    "Mist": 12
}
weather_risk += weather_weights.get(weather_condition, 8)

if visibility < 300:
    weather_risk += 15
if temp > 40:
    weather_risk += 10
if humidity > 85:
    weather_risk += 8
if wind_speed > 10:
    weather_risk += 10

# ---- Safety Risk ----
safety_risk += (100 - helmet_usage) * 0.25
safety_risk += (100 - seatbelt_usage) * 0.2
if speeding == "Yes":
    safety_risk += 15

# ---- TOTAL AI RISK ----
total_risk = traffic_risk + weather_risk + safety_risk

# Normalize to congestion %
congestion_percentage = min(100, int((total_risk / 170) * 100))

# ---------------- OUTPUT ----------------
st.subheader("📊 AI-Based Congestion Prediction")

st.metric("Traffic Congestion Level", f"{congestion_percentage}%")
st.progress(congestion_percentage / 100)

if congestion_percentage < 35:
    st.success("🟢 Low Congestion Risk")
elif congestion_percentage < 65:
    st.warning("🟡 Moderate Congestion Risk")
else:
    st.error("🔴 High Congestion Risk")

# ---------------- EXPLAINABILITY ----------------
st.subheader("🧠 AI Explanation")

st.write(f"🌡 Temperature: **{temp} °C**")
st.write(f"💧 Humidity: **{humidity}%**")
st.write(f"🌬 Wind Speed: **{wind_speed} m/s**")
st.write(f"👁 Visibility: **{visibility} meters**")
st.write(f"🌦 Weather Condition: **{weather_condition}**")

st.write("---")
st.write("**Risk Contribution**")
st.write(f"🚗 Traffic Risk: {int(traffic_risk)}")
st.write(f"🌦 Weather Risk: {int(weather_risk)}")
st.write(f"🛑 Safety Risk: {int(safety_risk)}")

st.subheader("🚦 Recommended Actions")

if congestion_percentage >= 65:
    st.write("• Trigger emergency traffic diversion")
    st.write("• Issue public alerts")
    st.write("• Increase enforcement")
elif congestion_percentage >= 35:
    st.write("• Adjust signal timings")
    st.write("• Warn commuters")
else:
    st.write("• Maintain normal operations")

st.caption("CongestiQ AI | Real-Time, Explainable Traffic Intelligence")

