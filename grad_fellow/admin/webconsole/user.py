# -*- coding:utf-8 -*-
"""User management."""
from flask import Blueprint, render_template

from ...models import User
from .auth import login_required

url_prefix = '/admin/user'
bp = Blueprint('user', __name__, url_prefix=url_prefix)
block_title = 'User Management'


@bp.route('/')
@login_required
def manage():
    """Manage user."""
    users = User.query.all()
    return render_template(
        'manage/user.html', block_title=block_title, users=users
    )
