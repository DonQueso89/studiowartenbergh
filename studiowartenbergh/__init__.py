import os
from .commands import commands
from flask import Flask
from .routes.routes import routes


# Application factory
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

    # Ensure existence of instance dir
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Register routes
    for view, route in routes:
        app.route(route)(view)

    # Register db commands
    from . import db
    app.teardown_appcontext(db.close_db)
    app.cli.add_command(db.init_db)

    # Register other commands
    for cmd in commands:
        app.cli.command()(cmd)

    from .routes.blueprints import auth, api, admin

    # Authentication for auth
    app.register_blueprint(auth.bp)

    # Read only API for retrieval
    app.register_blueprint(api.bp)

    # Content submission / modification
    app.register_blueprint(admin.bp)

    return app
