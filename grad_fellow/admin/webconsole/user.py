# -*- coding:utf-8 -*-
"""User management."""
from flask import Blueprint, abort, render_template
from flask_jwt import jwt_required

from grad_fellow.common.abort import abort_if_user_doesnt_exist
from grad_fellow.forms import AddUserForm, UpdateUserForm

bp = Blueprint('user', __name__, url_prefix='/admin/user')


@bp.route('/add')
@jwt_required()
def add_user():
    """Add user."""
    form = AddUserForm()
    return render_template('add_user.html', title='Add User', form=form)


@bp.route('/update/<string:name>')
@jwt_required()
def update_user(name):
    """Update user."""
    form = UpdateUserForm()
    user = abort_if_user_doesnt_exist(abort, name)
    return render_template('update_user.html', title='Update User',
                           form=form, uid=user.id, name=name, role=user.role)


@bp.route('/delete/<string:name>')
@jwt_required()
def delete_user(name):
    """Delete user."""
    from flask_wtf import FlaskForm
    abort_if_user_doesnt_exist(abort, name)
    form = FlaskForm()
    return render_template('delete_user.html', title='Delete User',
                           form=form, name=name)
