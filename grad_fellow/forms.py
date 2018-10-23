# -*- coding:utf-8 -*-
"""Forms."""
from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, RadioField, StringField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    """Login form."""

    username = StringField('User Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('remember me', default=False)


class AddUserForm(FlaskForm):
    """Add user form."""

    choices = [(0, 'Admin'), (1, 'User')]
    name = StringField('User Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    role = RadioField('Role', choices=choices, default=1,
                      validators=[DataRequired()])


class UpdateUserForm(FlaskForm):
    """Update user form."""

    id = StringField('User Id', validators=[DataRequired()])
    name = StringField('User Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    role = RadioField('Role', choices=AddUserForm.choices, default=1,
                      validators=[DataRequired()])


class AddCountryForm(FlaskForm):
    """Add country form."""

    name = StringField('Country Name', validators=[DataRequired()])


class UpdateCountryForm(FlaskForm):
    """Update country form."""

    id = StringField('Country Id', validators=[DataRequired()])
    name = StringField('Country Name', validators=[DataRequired()])


class AddPositionForm(FlaskForm):
    """Add position form."""

    name = StringField('Position Name', validators=[DataRequired()])


class UpdatePositionForm(FlaskForm):
    """Update position form."""

    id = StringField('Position Id', validators=[DataRequired()])
    name = StringField('Position Name', validators=[DataRequired()])
