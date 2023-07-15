from flask import Flask
from flask_mongoengine import MongoEngine


# Globally accessible libraries
db = MongoEngine()

def create_app():
    """Initialize the core application."""
    app = Flask(__name__, instance_relative_config=False)

    # Using a production configuration
    app.config.from_object('config.Config')

    # Initialize Plugins
    db.init_app(app)

    with app.app_context():

        # Include our Routes
        from . import routes

        # Include & Register Blueprints
        from .auth import routes_auth
        app.register_blueprint(routes_auth.auth_bp)

        # Include & Register Blueprints
        from .home import routes_home
        app.register_blueprint(routes_home.home_bp)

        # Include & Register Blueprints
        from .prometheus import routes_prometheus
        app.register_blueprint(routes_prometheus.prometheus_bp)        

        return app