# -*- coding:utf-8 -*-
"""User management."""
from flask import Blueprint, render_template

from ...models import User
from .auth import login_required

bp = Blueprint('user', __name__, url_prefix='/admin/user')


@bp.route('/')
@login_required
def manage():
    """Manage user."""
    users = User.query.all()
    return render_template('manage/user.html', users=users)
