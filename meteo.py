import requests
import json
from datetime import datetime

API_URL = "https://api.open-meteo.com/v1/forecast"

CITIES = {
    "Paris": {"latitude": 48.8566, "longitude": 2.3522, "timezone": "Europe/Paris"},
    "Lyon": {"latitude": 45.7640, "longitude": 4.8357, "timezone": "Europe/Paris"},
}

def get_params(latitude, longitude, timezone):
    return {
        "latitude": latitude,
        "longitude": longitude,
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
        "timezone": timezone,
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

def fetch_weather(city, latitude, longitude, timezone):
    """Récupère les données météo pour une ville"""
    params = get_params(latitude, longitude, timezone)
    print(f"Récupération de la météo de {city}...")
    response = requests.get(API_URL, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()
    
    current = data["current"]
    hourly = data["hourly"]
    daily = data["daily"]
    
    weather_code = current.get("weather_code", 0)
    wind_deg = current.get("wind_direction_10m", 0)
    
    result = {
        "city": city,
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
    
    # Affichage du résumé
    print(f"  Température   : {result['current']['temperature']}°C (ressentie {result['current']['apparent_temperature']}°C)")
    print(f"  Humidité      : {result['current']['humidity']}%")
    print(f"  Précipitations: {result['current']['precipitation']} mm")
    print(f"  Vent          : {result['current']['wind_speed']} km/h {result['current']['wind_direction']}")
    print(f"  Conditions    : {result['current']['weather_description']}\n")
    
    return result

# Récupération des données pour toutes les villes
results = []
for city, coords in CITIES.items():
    weather_data = fetch_weather(city, coords["latitude"], coords["longitude"], coords["timezone"])
    results.append(weather_data)

# Sauvegarde dans un fichier JSON
with open("meteo.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print("Données sauvegardées dans meteo.json")
