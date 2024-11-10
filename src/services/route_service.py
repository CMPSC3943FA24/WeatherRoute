# services/route_service.py
import googlemaps
from datetime import datetime, timedelta
from typing import List, Dict
from config.settings import Config
from services.weather_service import get_weather_forecast

def get_route_cities(origin: str, destination: str, api_key: str) -> List[Dict]:
    gmaps = googlemaps.Client(key=api_key)

    try:
        # Get the route
        now = datetime.now()
        directions_result = gmaps.directions(origin, destination, 
                                             mode="driving",
                                             departure_time=now)

        if not directions_result:
            raise Exception("No route found")

        route = directions_result[0]
        
        # Extract total duration from the route
        total_duration = sum(leg['duration']['value'] for leg in route['legs']) / 3600  # Convert to hours

        route_cities = []
        current_time = now

        for leg in route['legs']:
            for step in leg['steps']:
                # Calculate ETA for this step
                step_duration = step['duration']['value'] / 3600  # Convert to hours
                current_time += timedelta(hours=step_duration)
                
                # Get the end location of this step
                end_location = step['end_location']
                
                # Use reverse geocoding to get the city name
                geocode_result = gmaps.reverse_geocode((end_location['lat'], end_location['lng']))
                
                city = None
                state = None
                for component in geocode_result[0]['address_components']:
                    if 'locality' in component['types']:
                        city = component['long_name']
                    if 'administrative_area_level_1' in component['types']:
                        state = component['short_name']
                
                if city and state:
                    # Check if this city is already in our list
                    if not any(c['name'] == city for c in route_cities):
                        weather = get_weather_forecast(city, state, current_time)
                        route_cities.append({
                            'name': city,
                            'state': state,
                            'arrival_time': current_time.strftime("%Y-%m-%d %H:%M:%S"),
                            'weather': weather
                        })

        return route_cities

    except googlemaps.exceptions.ApiError as e:
        raise Exception(f"Google Maps API Error: {e}")
    except Exception as e:
        raise Exception(f"Unexpected error: {e}")