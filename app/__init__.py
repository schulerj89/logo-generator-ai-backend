# -*- coding: utf-8 -*-
"""Initialize Flask app."""
from flask import Flask
from flask_cors import CORS
from .routes import main_routes

def create_app():
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__)
    CORS(app)

    # Register Blueprints (routes)
    app.register_blueprint(main_routes)

    return app
