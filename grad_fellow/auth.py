# -*- coding:utf-8 -*-
"""Authentication."""
import logging

from flask_jwt import JWT
from sqlalchemy.exc import OperationalError
from werkzeug.security import check_password_hash

from .common.acl import check_access_permission
from .models import Administrator, User

logger = logging.getLogger(__name__)


def init_app(app):
    """Init authentication."""
    jwt = JWT(app, _authenticate, _identity)
    return jwt


def _authenticate(username, password):
    """Authenticate handler."""
    logger.debug('authenticate: {}:{}'.format(username, '*' * len(password)))
    user = User4Auth(username)
    if not user.verify_password(password):
        logger.info('fail')
        return
    return user


def _identity(payload):
    """Identity handler."""
    user_id = payload['identity']
    username = user_id[0]
    logger.info('username: ' + username)
    password = user_id[1]
    if not check_access_permission(username):
        return None
    user = None
    if username == 'admin':
        try:
            user = Administrator.query.filter_by(name=username).first()
        except OperationalError as e:
            logger.error(str(e))
    else:
        try:
            user = User.query.filter_by(name=username).first()
        except OperationalError as e:
            logger.error(str(e))
    if user and password == user.password:
        return User4Auth(username)
    return None


def _verify_admin_password(user_name, password):
    return __verify_password(Administrator, user_name, password)


def _verify_user_password(user_name, password):
    return __verify_password(User, user_name, password)


def __verify_password(model, user_name, password):
    try:
        user = model.query.filter_by(name=user_name).first()
    except OperationalError as e:
        logger.error(str(e))
        return False
    if not user:
        return False
    return check_password_hash(user.password, password)


class User4Auth(object):
    """User for auth."""

    def __init__(self, username):
        """Init User4Auth instance."""
        self.username = username
        self.id = self.get_id()

    def __repr__(self):
        """Provide usable string representations of itself."""
        return '<User4Auth %r>' % self.username

    def get_id(self):
        """Get identification."""
        user = None
        if self.username == 'admin':
            try:
                user = Administrator.query.filter_by(
                    name=self.username).first()
            except OperationalError as e:
                logger.error(str(e))
        else:
            try:
                user = User.query.filter_by(name=self.username).first()
            except OperationalError as e:
                logger.error(str(e))
        password = user and user.password
        return [self.username, password]

    def verify_password(self, password):
        """Verify password."""
        if self.username == 'admin':
            return _verify_admin_password(self.username, password)
        else:
            return _verify_user_password(self.username, password)
