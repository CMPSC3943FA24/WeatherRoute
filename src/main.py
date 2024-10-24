from flask import Flask
from api.routes import route_bp
import logging
from config.settings import Config

logging.basicConfig(level=Config.LOG_LEVEL, format=Config.LOG_FORMAT)

app = Flask(__name__)
app.register_blueprint(route_bp)

if __name__ == "__main__":
    app.run(debug=True)