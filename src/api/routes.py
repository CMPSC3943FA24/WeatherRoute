from flask import Blueprint, request, jsonify
from services.route_service import get_route_cities
from config.settings import Config

route_bp = Blueprint('route', __name__)

@route_bp.route('/get_cities', methods=['GET'])
def cities_on_route():
    origin = request.args.get('origin')
    destination = request.args.get('destination')

    if not origin or not destination:
        return jsonify({"error": "Origin and destination are required"}), 400

    try:
        cities = get_route_cities(origin, destination, Config.GOOGLE_MAPS_API_KEY)
        return jsonify({
            "origin": origin,
            "destination": destination,
            "cities": [city['name'] for city in cities]
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500