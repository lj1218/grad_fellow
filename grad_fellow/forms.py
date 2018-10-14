# -*- coding:utf-8 -*-
# forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField, RadioField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField('User Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('remember me', default=False)


class AddUserForm(FlaskForm):
    choices = [(0, 'Admin'), (1, 'User')]
    name = StringField('User Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    role = RadioField('Role', choices=choices, default=1, validators=[DataRequired()])


class UpdateUserForm(FlaskForm):
    id = StringField('User Id', validators=[DataRequired()])
    name = StringField('User Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    role = RadioField('Role', choices=AddUserForm.choices, default=1, validators=[DataRequired()])


class AddCountryForm(FlaskForm):
    name = StringField('Country Name', validators=[DataRequired()])


class UpdateCountryForm(FlaskForm):
    id = StringField('Country Id', validators=[DataRequired()])
    name = StringField('Country Name', validators=[DataRequired()])


class AddPositionForm(FlaskForm):
    name = StringField('Position Name', validators=[DataRequired()])


class UpdatePositionForm(FlaskForm):
    id = StringField('Position Id', validators=[DataRequired()])
    name = StringField('Position Name', validators=[DataRequired()])
