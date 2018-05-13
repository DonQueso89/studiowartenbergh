import os
from .commands import commands
from flask import Flask
from .db import close_db
from .routes.routes import routes


def create_app(test_config=None):
    app = Flask("studiowartenbergh", instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'studiowartenbergh.sqlite')
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    # Register routes
    for view, route in routes:
        app.route(route)(view)

    # Register commands
    for cmd in commands:
        app.cli.command()(cmd)

    app.teardown_appcontext(close_db)

    return app
