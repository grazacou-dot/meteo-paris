import requests
import json
from datetime import datetime

LATITUDE = 48.8566
LONGITUDE = 2.3522
CITY = "Paris"
API_URL = "https://api.open-meteo.com/v1/forecast"

params = {
    "latitude": LATITUDE,
    "longitude": LONGITUDE,
    "current": [
        "temperature_2m",
        "apparent_temperature",
        "precipitation",
        "wind_speed_10m",
        "wind_direction_10m",
        "weather_code",
        "relative_humidity_2m",
    ],
    "hourly": ["temperature_2m", "precipitation_probability"],
    "daily": ["temperature_2m_max", "temperature_2m_min", "precipitation_sum"],
    "timezone": "Europe/Paris",
    "forecast_days": 3,
}

WMO_CODES = {
    0: "Ciel dégagé", 1: "Principalement dégagé", 2: "Partiellement nuageux", 3: "Couvert",
    45: "Brouillard", 48: "Brouillard givrant",
    51: "Bruine légère", 53: "Bruine modérée", 55: "Bruine dense",
    61: "Pluie légère", 63: "Pluie modérée", 65: "Pluie forte",
    71: "Neige légère", 73: "Neige modérée", 75: "Neige forte",
    80: "Averses légères", 81: "Averses modérées", 82: "Averses violentes",
    95: "Orage", 96: "Orage avec grêle", 99: "Orage violent avec grêle",
}

def wind_direction_label(degrees):
    directions = ["N", "NE", "E", "SE", "S", "SO", "O", "NO"]
    return directions[round(degrees / 45) % 8]

print(f"Récupération de la météo de {CITY}...")
response = requests.get(API_URL, params=params, timeout=10)
response.raise_for_status()
data = response.json()

current = data["current"]
hourly = data["hourly"]
daily = data["daily"]

weather_code = current.get("weather_code", 0)
wind_deg = current.get("wind_direction_10m", 0)

result = {
    "city": CITY,
    "retrieved_at": datetime.now().isoformat(),
    "current": {
        "temperature": current["temperature_2m"],
        "apparent_temperature": current["apparent_temperature"],
        "humidity": current["relative_humidity_2m"],
        "precipitation": current["precipitation"],
        "wind_speed": current["wind_speed_10m"],
        "wind_direction_deg": wind_deg,
        "wind_direction": wind_direction_label(wind_deg),
        "weather_code": weather_code,
        "weather_description": WMO_CODES.get(weather_code, "Inconnu"),
    },
    "hourly": {
        "time": hourly["time"][:24],
        "temperature": hourly["temperature_2m"][:24],
        "precipitation_probability": hourly["precipitation_probability"][:24],
    },
    "daily": {
        "time": daily["time"],
        "temp_max": daily["temperature_2m_max"],
        "temp_min": daily["temperature_2m_min"],
        "precipitation_sum": daily["precipitation_sum"],
    },
}

with open("meteo.json", "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print(f"  Température   : {result['current']['temperature']}°C (ressentie {result['current']['apparent_temperature']}°C)")
print(f"  Humidité      : {result['current']['humidity']}%")
print(f"  Précipitations: {result['current']['precipitation']} mm")
print(f"  Vent          : {result['current']['wind_speed']} km/h {result['current']['wind_direction']}")
print(f"  Conditions    : {result['current']['weather_description']}")
print("Données sauvegardées dans meteo.json")
