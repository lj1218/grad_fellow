# -*- coding:utf-8 -*-
"""Auth for web console."""
import functools
import json
import logging

from flask import (Blueprint, g, redirect, render_template, request, session,
                   url_for)

from ...auth import User4Auth
from ...models import Administrator

logger = logging.getLogger(__name__)
bp = Blueprint('auth', __name__, url_prefix='/auth')


def login_required(view):
    """View decorator that redirects anonymous users to the login page."""
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)

    return wrapped_view


@bp.before_app_request
def load_logged_in_user():
    """Load logged in user.

    If a username is stored in the session, load the user object from
    the database into ``g.user``.
    """
    username = session.get('name')
    if not request.path.startswith('/static/'):
        logger.debug('load_logged_in_user: ' + str(username))

    if username is None:
        g.user = None
    else:
        g.user = Administrator.query.filter_by(name=username).first()


@bp.route('/login', methods=('GET', 'POST'))
def login():
    """Log in a registered user by adding the user id to the session."""
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        error = None
        if username != 'admin':
            error = 'Incorrect username.'
        elif not User4Auth(username).verify_password(password):
            error = 'Incorrect password.'

        status_code = 200
        if error is None:
            # store the username in a new session and return to the index
            session.clear()
            session['name'] = username
            result = {'status': 0, 'next': url_for('index')}
        else:
            status_code = 401
            result = {'status': 1, 'error': error}

        logger.info(json.dumps(result))
        return json.dumps(result), status_code, \
            {'Content-Type': 'application/json'}

    return render_template('auth/login.html')


@bp.route('/logout')
@login_required
def logout():
    """Clear the current session, including the stored username."""
    session.clear()
    return redirect(url_for('index'))
