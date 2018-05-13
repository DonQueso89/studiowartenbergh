import click
from .db import get_db
from flask import current_app


def init_db():
    db = get_db()
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

    click.echo('Initialized database')


def test():
    click.echo("test command")


commands = (
    test,
    init_db,
)
