from flask import Flask
from flask_migrate import Migrate
from app.config import Config
from app.extensions import db

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize database and migrations
    db.init_app(app)
    Migrate(app, db)

    # Import and register Blueprints
    from app.routes.customers import customer_bp
    from app.routes.products import product_bp
    from app.routes.orders import order_bp

    app.register_blueprint(customer_bp, url_prefix='/customers')
    app.register_blueprint(product_bp, url_prefix='/products')
    app.register_blueprint(order_bp, url_prefix='/orders')

    return app
