from flask import Flask

# Globally accessible libraries
#db = SQLAlchemy()

def create_app():
    """Initialize the core application."""
    app = Flask(__name__, instance_relative_config=False)

    # Using a production configuration
    #app.config.from_object('config.ProdConfig')

    # Using a development configuration
    app.config.from_object('config.DevConfig')

    # Initialize Plugins
    #db.init_app(app)

    with app.app_context():

        # Include our Routes
        from . import routes

        # Include & Register Blueprints
        from .authentication import routes
        app.register_blueprint(routes.auth_bp)

        # Include & Register Blueprints
        from .home import routes
        app.register_blueprint(routes.home_bp)

        # Include & Register Blueprints
        from .prometheus import routes
        app.register_blueprint(routes.prometheus_bp)        

        return app