# -*- coding:utf-8 -*-
"""Database module."""
import click
from flask.cli import with_appcontext
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Initialize the database."""
    db.drop_all()
    db.create_all()
    click.echo('Initialized the database.')


def init_app(app):
    """Init database module."""
    db.init_app(app)
    # register database functions with the Flask app
    app.cli.add_command(init_db_command)
