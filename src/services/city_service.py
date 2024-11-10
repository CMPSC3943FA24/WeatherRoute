import time
import requests
from typing import List, Dict, Tuple, Optional
from config.settings import Config

class OverpassAPIError(Exception):
    pass

def create_overpass_query(bounds: Tuple[float, float, float, float], min_population: int) -> str:
    south, west, north, east = bounds
    return f"""[out:json];
node
  ["place"~"city|town"]
  ["population"]
  ({south},{west},{north},{east})
  ["population"~"^[0-9]+$"]
  ["population"!~"^0+$"];
out body;"""

def get_cities_in_chunk(chunk_points: List[tuple]) -> List[Dict]:
    if not chunk_points:
        return []

    try:
        lats, lons = zip(*[(float(p[0]), float(p[1])) for p in chunk_points])
        south = min(lats)
        north = max(lats)
        west = min(lons)
        east = max(lons)
        bounds = (south, west, north, east)
        
        if not all(-90 <= x <= 90 for x in [south, north]) or \
           not all(-180 <= x <= 180 for x in [west, east]):
            raise ValueError("Coordinates out of valid range")
            
    except (ValueError, TypeError) as e:
        raise OverpassAPIError(f"Invalid coordinates: {e}")

    overpass_url = "https://overpass-api.de/api/interpreter"
    query = create_overpass_query(bounds, Config.MIN_POPULATION)
    
    for attempt in range(3):
        try:
            time.sleep(1)
            response = requests.post(
                overpass_url, 
                data={"data": query}, 
                timeout=30,
                headers={"Accept": "application/json"}
            )
            
            response.raise_for_status()
            data = response.json()
            
            if 'elements' not in data:
                return []
                
            cities = []
            for element in data['elements']:
                city_info = parse_city_element(element)
                if city_info and city_info['population'] >= Config.MIN_POPULATION:
                    cities.append(city_info)
                    
            return cities
            
        except requests.exceptions.RequestException as e:
            if attempt == 2:
                raise OverpassAPIError(f"Overpass API request failed after 3 attempts: {str(e)}")
            time.sleep(2 ** attempt)

def parse_city_element(element: Dict) -> Optional[Dict]:
    try:
        tags = element.get('tags', {})
        
        if 'name' not in tags or 'population' not in tags:
            return None
            
        try:
            population = int(tags['population'])
            if population <= 0:
                return None
        except (ValueError, TypeError):
            return None
            
        return {
            'name': tags['name'],
            'lat': element['lat'],
            'lon': element['lon'],
            'state': tags.get('addr:state', ''),
            'country': tags.get('addr:country', 'US'),
            'population': population
        }
    except Exception:
        return None