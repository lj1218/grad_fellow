# -*- coding:utf-8 -*-
"""Administrator management."""
from flask import Blueprint, render_template

from .auth import login_required

bp = Blueprint('administrator', __name__, url_prefix='/admin/administrator')


@bp.route('/')
@login_required
def manage():
    """Manage administrator."""
    return render_template('manage/administrator.html')
