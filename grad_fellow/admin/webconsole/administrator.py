# -*- coding:utf-8 -*-
"""Administrator management."""
from flask import Blueprint, render_template

from .auth import login_required

url_prefix = '/admin/administrator'
bp = Blueprint('administrator', __name__, url_prefix=url_prefix)
block_title = 'Administrator Management'


@bp.route('/')
@login_required
def manage():
    """Manage administrator."""
    return render_template(
        'manage/administrator.html', block_title=block_title
    )
