# -*- coding:utf-8 -*-
"""Set password for administrator."""
import logging

import click
from flask.cli import with_appcontext
from sqlalchemy.exc import OperationalError
from werkzeug.security import generate_password_hash

from ..db import db
from ..models import Administrator

logger = logging.getLogger(__name__)


@click.command('set-admin-password')
@click.option('--password', default='1', prompt='password',
              help='Set password for admin.')
@with_appcontext
def set_admin_password(password):
    """Set password for admin."""
    try:
        admin = Administrator.query.filter_by(name='admin').first()
    except OperationalError as e:
        logger.error(str(e))
        return False

    password_hash = generate_password_hash(password)
    if not admin:
        admin = Administrator(name='admin', password=password_hash)
    else:
        admin.password = password_hash

    db.session.add(admin)
    try:
        db.session.commit()
    except OperationalError as e:
        logger.error(str(e))
        return False
    print('set password to {} success'.format(password))
    return True


def init_app(app):
    """Init admin.passwd module."""
    app.cli.add_command(set_admin_password)
