from flask import Blueprint, request, jsonify
from services.route_service import create_route
from config.settings import Config

route_bp = Blueprint('route', __name__)

@route_bp.route('/create_route', methods=['POST'])
def route_creation():
    origin = request.json.get('origin')
    destination = request.json.get('destination')

    if not origin or not destination:
        return jsonify({"error": "Origin and destination are required"}), 400

    try:
        route_data = create_route(origin, destination, Config.GOOGLE_MAPS_API_KEY)
        return jsonify(route_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500