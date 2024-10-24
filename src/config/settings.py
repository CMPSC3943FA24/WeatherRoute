import os

class Config:
    GOOGLE_MAPS_API_KEY = os.environ.get('GOOGLE_MAPS_API_KEY', 'AIzaSyCVjS-nxFck0ktz6HL3bLYSGIJ5jH_3fOc')
    MIN_POPULATION = 10000
    CHUNK_SIZE = 100
    LOG_LEVEL = 'INFO'
    LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'