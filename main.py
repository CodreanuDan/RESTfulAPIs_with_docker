import requests
import os
from common_data import DataContainer
from datetime import datetime
from bat_runner import BatRunner

# Inițializezi DataContainer
param = DataContainer(location="Bacau", date=datetime.now())
rc = param.rc

# Obții URL-ul și cheia API
weather_api_url = param.WEATHER_API[0]  # Primary API

br = BatRunner()
try:
    br.bat_runner()
except Exception as e:
    print(f"❌ Error durring .bat setup: {e}")

api_key = os.getenv("WEATHER_API_KEY") 

# Construiești request-ul
params = {
    "q": param.location,
    "appid": api_key,
    "units": "metric"
}

# Trimiți request-ul
response = requests.get(weather_api_url, params=params)

# Verifici răspunsul
if response.status_code == rc["OK"]:
    data = response.json()
    print("🌤️ Weather Data:", data)
else:
    print(f"❌ Error {response.status_code}: {response.text}")





