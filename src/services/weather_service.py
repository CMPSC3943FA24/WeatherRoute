# services/weather_service.py
import requests
from datetime import datetime
from config.settings import Config

def get_weather_forecast(city: str, state: str, arrival_time: datetime) -> dict:
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city},{state}&appid={Config.OPENWEATHERMAP_API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        for forecast in data['list']:
            forecast_time = datetime.fromtimestamp(forecast['dt'])
            if forecast_time >= arrival_time:
                return {
                    "temperature": forecast['main']['temp'],
                    "description": forecast['weather'][0]['description']
                }
    return None