import time
import requests
from typing import List, Dict
from config.settings import Config

def get_cities_in_chunk(chunk_points: List[tuple]) -> List[Dict]:
    lats, lons = zip(*chunk_points)
    south, north, west, east = min(lats), max(lats), min(lons), max(lons)

    overpass_url = "https://overpass-api.de/api/interpreter"
    query = f"""
        [out:json];
        node["place"~"city|town"]["population"](if:number(t["population"]) > {Config.MIN_POPULATION})
        ({south},{west},{north},{east});
        out body;
        >;
        out skel qt;
    """

    time.sleep(1)

    try:
        response = requests.post(overpass_url, data=query)
        response.raise_for_status()
        data = response.json()
        return [create_city_info(element) for element in data.get('elements', [])
                if all(key in element.get('tags', {}) for key in ['name', 'population'])]
    except requests.exceptions.RequestException as e:
        print(f"Overpass API request failed: {e}")
        return []

def create_city_info(element: Dict) -> Dict:
    tags = element['tags']
    return {
        'name': tags['name'],
        'lat': element['lat'],
        'lon': element['lon'],
        'state': tags.get('addr:state', ''),
        'country': tags.get('addr:country', 'US'),
        'population': int(tags['population'])
    }