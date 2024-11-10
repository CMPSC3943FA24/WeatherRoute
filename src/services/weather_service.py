# services/weather_service.py
import requests
import logging
from datetime import datetime
from config.settings import Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_weather_forecast(city: str, state: str, arrival_time: datetime) -> dict:
    logger.info("Retrieving weather details for '%s' at '%s'",city,arrival_time)
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city},{state}&appid={Config.OPENWEATHERMAP_API_KEY}&units=imperial"
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