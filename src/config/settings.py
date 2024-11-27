import os

class Config:
    GOOGLE_MAPS_API_KEY = os.environ.get('GOOGLE_MAPS_API_KEY', 'AIzaSyCZCUFu-JD6uAsy-F_lepi7-2gW_6FUDo4')
    OPENWEATHERMAP_API_KEY = "23d244556b2492d0e22311c584f9d917"
    MIN_POPULATION = 10000
    CHUNK_SIZE = 100
    LOG_LEVEL = 'INFO'
    LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'