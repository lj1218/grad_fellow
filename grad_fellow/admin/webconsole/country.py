# -*- coding:utf-8 -*-
"""Country management."""
from flask import Blueprint, render_template, url_for

from ...models import Country
from .auth import login_required

bp = Blueprint('country', __name__, url_prefix='/admin/country')


@bp.route('/')
@login_required
def manage():
    """Manage country."""
    countries = Country.query.all()
    return render_template(
        'manage/country.html', title='Manage Country',
        block_title='Country Management', table_id='positionTable',
        endpoint='country', items=countries,
        manage_page_url=url_for('country.manage'),
        item_label_name='Country name', manage_btn_name='Add Country'
    )
