import googlemaps
import polyline
from typing import List, Dict
from config.settings import Config
from services.city_service import get_cities_in_chunk
from utils.distance_calculator import calculate_distance

def get_route_cities(origin: str, destination: str, api_key: str) -> List[Dict]:
    gmaps = googlemaps.Client(key=api_key)

    try:
        route = gmaps.directions(origin, destination)[0]
        points = polyline.decode(route['overview_polyline']['points'])

        origin_lat, origin_lon = points[0]
        route_cities = []
        for i in range(0, len(points), Config.CHUNK_SIZE):
            chunk_points = points[i:i + Config.CHUNK_SIZE]
            cities_in_chunk = get_cities_in_chunk(chunk_points)
            for city in cities_in_chunk:
                city['distance_from_origin'] = calculate_distance(origin_lat, origin_lon, city['lat'], city['lon'])
            route_cities.extend(cities_in_chunk)

        unique_cities = {}
        for city in route_cities:
            city_key = f"{city['name']}, {city['state'] or city['country']}"
            if city_key not in unique_cities or city['distance_from_origin'] < unique_cities[city_key]['distance_from_origin']:
                unique_cities[city_key] = city

        return sorted(unique_cities.values(), key=lambda x: x['distance_from_origin'])

    except googlemaps.exceptions.ApiError as e:
        raise Exception(f"Google Maps API Error: {e}")
    except Exception as e:
        raise Exception(f"Unexpected error: {e}")