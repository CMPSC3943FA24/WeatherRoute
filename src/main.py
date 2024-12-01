from flask import Flask
from flask_cors import CORS
from api.routes import route_bp
import logging
from config.settings import Config

logging.basicConfig(level=Config.LOG_LEVEL, format=Config.LOG_FORMAT)

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
app.register_blueprint(route_bp)

if __name__ == "__main__":
    app.run(debug=True)