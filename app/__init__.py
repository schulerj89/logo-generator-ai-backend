# -*- coding: utf-8 -*-
"""Initialize Flask app."""
import os
from flask import Flask
from flask_caching import Cache
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_cors import CORS
from .routes import main_routes

def create_app():
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__)
    CORS(app)

    # Configure and initialize cache
    cache = Cache(config={
        "CACHE_TYPE": "RedisCache",      # Use 'RedisCache' for Redis; 'SimpleCache' for local dev
        "CACHE_REDIS_URL": f"redis://{os.getenv('REDIS_URL')}/0",
        "CACHE_DEFAULT_TIMEOUT": 300
    })
    cache.init_app(app)

    # Initialize the limiter (applied by IP address by default)
    limiter = Limiter(get_remote_address, default_limits=["100 per minute"])  # Adjust as needed
    limiter.init_app(app)

    # Register Blueprints (routes)
    app.register_blueprint(main_routes)

    app.cache = cache
    app.limiter = limiter

    return app
