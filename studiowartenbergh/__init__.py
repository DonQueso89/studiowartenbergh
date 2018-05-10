from flask import Flask
from .routes.routes import routes


def create_app():
    app = Flask("studiowartenbergh")
    for view, route in routes:
        app.route(route)(view)
    return app
