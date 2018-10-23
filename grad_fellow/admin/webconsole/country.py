# -*- coding:utf-8 -*-
"""Country management."""
from flask import Blueprint, abort, render_template
from flask_jwt import jwt_required

from grad_fellow.common.abort import abort_if_country_doesnt_exist
from grad_fellow.forms import AddCountryForm, UpdateCountryForm

bp = Blueprint('country', __name__, url_prefix='/admin/country')


@bp.route('/add')
@jwt_required()
def add_country():
    """Add country."""
    form = AddCountryForm()
    return render_template('add_country.html', title='Add Country', form=form)


@bp.route('/update/<int:country_id>')
@jwt_required()
def update_country(country_id):
    """Update country."""
    abort_if_country_doesnt_exist(abort, country_id)
    form = UpdateCountryForm()
    return render_template('update_country.html', title='Update Country',
                           form=form, country_id=country_id)


@bp.route('/delete/<int:country_id>')
@jwt_required()
def delete_country(country_id):
    """Delete country."""
    from flask_wtf import FlaskForm
    abort_if_country_doesnt_exist(abort, country_id)
    form = FlaskForm()
    return render_template('delete_country.html', title='Delete Country',
                           form=form, country_id=country_id)
