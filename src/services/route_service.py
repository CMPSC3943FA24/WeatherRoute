import googlemaps
from datetime import datetime, timedelta
from typing import List, Dict
import logging
from services.city_service import OverpassAPIError, get_cities_in_chunk
from services.weather_service import get_weather_forecast
from utils.distance_calculator import calculate_distance

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_route(origin: str, destination: str, api_key: str) -> Dict:
    gmaps = googlemaps.Client(key=api_key)

    try:
        directions_result = gmaps.directions(origin, destination, mode="driving", departure_time=datetime.now())
        
        if not directions_result:
            raise Exception("No route found")

        route = directions_result[0]

        estimated_duration = route['legs'][0]['duration']['value']

        total_distance_meters = route['legs'][0]['distance']['value']
        total_distance_miles = total_distance_meters * 0.000621371
        
        cities = get_route_cities(origin, destination, api_key)
        
        cities_with_weather = []
        departure_time = datetime.now()
        for city in cities:
            travel_time = timedelta(hours=city['distance_from_origin'] / 100)
            eta = departure_time + travel_time
            
            weather = get_weather_forecast(city['name'], city['state'], eta)
            
            cities_with_weather.append({
                'name': city['name'],
                'state': city['state'],
                'lat': city['lat'],
                'lon': city['lon'],
                'eta': eta.isoformat(),
                'weather': weather
            })

        return {
            'origin': origin,
            'destination': destination,
            'estimatedDuration': estimated_duration,
            'totalDistance': total_distance_miles,
            'cities': cities_with_weather,
            'polyline': route['overview_polyline']['points']
        }

    except googlemaps.exceptions.ApiError as e:
        raise Exception(f"Google Maps API Error: {e}")
    except Exception as e:
        raise Exception(f"Unexpected error: {e}")

def get_route_cities(origin: str, destination: str, api_key: str) -> List[Dict]:
    logger.info("Processing route from '%s' to '%s'", origin, destination)
    
    gmaps = googlemaps.Client(key=api_key)
    
    try:
        directions_result = gmaps.directions(origin, destination)
        if not directions_result:
            raise ValueError(f"No route found between {origin} and {destination}")
            
        route = directions_result[0]
        points = googlemaps.convert.decode_polyline(route['overview_polyline']['points'])
        
        if not points:
            raise ValueError("No valid points found in route polyline")
            
        try:
            origin_lat = float(points[0]['lat'])
            origin_lon = float(points[0]['lng'])
            dest_lat = float(points[-1]['lat'])
            dest_lon = float(points[-1]['lng'])
        except (KeyError, ValueError, TypeError) as e:
            raise ValueError(f"Invalid coordinates: {e}")
        
        route_cities = []
        chunk_size = 10
        
        chunks = [points[i:i + chunk_size] for i in range(0, len(points), chunk_size)]
        
        for chunk in chunks:
            chunk_points = [
                (
                    float(point['lat']), 
                    float(point['lng'])
                ) 
                for point in chunk 
                if 'lat' in point and 'lng' in point
            ]
            
            if not chunk_points:
                continue
                
            try:
                cities_in_chunk = get_cities_in_chunk(chunk_points)
                
                for city in cities_in_chunk:
                    city['distance_from_origin'] = calculate_distance(
                        origin_lat, 
                        origin_lon, 
                        city['lat'], 
                        city['lon']
                    )
                    
                route_cities.extend(cities_in_chunk)
                
            except OverpassAPIError:
                continue
        
        # Add destination city
        dest_info = gmaps.reverse_geocode((dest_lat, dest_lon))
        if dest_info:
            dest_city = next((component for component in dest_info[0]['address_components'] 
                              if 'locality' in component['types']), None)
            dest_state = next((component for component in dest_info[0]['address_components'] 
                               if 'administrative_area_level_1' in component['types']), None)
            if dest_city:
                dest_city_info = {
                    'name': dest_city['long_name'],
                    'state': dest_state['short_name'] if dest_state else '',
                    'lat': dest_lat,
                    'lon': dest_lon,
                    'distance_from_origin': calculate_distance(origin_lat, origin_lon, dest_lat, dest_lon)
                }
                route_cities.append(dest_city_info)

        filtered_cities = []
        last_added_city = None
        
        for city in route_cities:
            if last_added_city is None or calculate_distance(
                last_added_city['lat'], last_added_city['lon'],
                city['lat'], city['lon']
            ) >= 40:  # Check if distance is at least 40 miles
                filtered_cities.append(city)
                last_added_city = city

        unique_cities = {}
        for city in filtered_cities:
            city_key = f"{city['name']}, {city['state'] or ''}"
            if (city_key not in unique_cities or 
                city['distance_from_origin'] < unique_cities[city_key]['distance_from_origin']):
                unique_cities[city_key] = city
        
        sorted_cities = sorted(
            unique_cities.values(), 
            key=lambda x: x['distance_from_origin']
        )
        
        logger.info("Processing complete. Found %d unique cities along the route", len(sorted_cities))
        return sorted_cities
        
    except googlemaps.exceptions.ApiError as e:
        raise
    except Exception as e:
        raise ValueError(f"Failed to process route: {str(e)}")