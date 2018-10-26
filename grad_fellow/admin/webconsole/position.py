# -*- coding:utf-8 -*-
"""Position management."""
from flask import Blueprint, render_template, url_for

from ...models import Position
from .auth import login_required

bp = Blueprint('position', __name__, url_prefix='/admin/position')


@bp.route('/')
@login_required
def manage():
    """Manage position."""
    positions = Position.query.all()
    return render_template(
        'manage/position.html', title='Manage Position',
        block_title='Position Management', table_id='positionTable',
        endpoint='position', items=positions,
        manage_page_url=url_for('position.manage'),
        item_label_name='Position name', manage_btn_name='Add Position'
    )
