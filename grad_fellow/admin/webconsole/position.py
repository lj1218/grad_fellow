# -*- coding:utf-8 -*-
"""Position management."""
from flask import Blueprint, abort, render_template
from flask_jwt import jwt_required

from grad_fellow.common.abort import abort_if_position_doesnt_exist
from grad_fellow.forms import AddPositionForm, UpdatePositionForm

bp = Blueprint('position', __name__, url_prefix='/admin/position')


@bp.route('/add')
@jwt_required()
def add_position():
    """Add position."""
    form = AddPositionForm()
    return render_template('add_position.html', title='Add Position',
                           form=form)


@bp.route('/update/<int:position_id>')
@jwt_required()
def update_position(position_id):
    """Update position."""
    abort_if_position_doesnt_exist(abort, position_id)
    form = UpdatePositionForm()
    return render_template('update_position.html', title='Update Position',
                           form=form, position_id=position_id)


@bp.route('/delete/<int:position_id>')
@jwt_required()
def delete_position(position_id):
    """Delete position."""
    from flask_wtf import FlaskForm
    abort_if_position_doesnt_exist(abort, position_id)
    form = FlaskForm()
    return render_template('delete_position.html', title='Delete Position',
                           form=form, position_id=position_id)
