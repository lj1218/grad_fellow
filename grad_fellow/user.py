# -*- coding:utf-8 -*-
from flask import render_template
from flask_jwt import jwt_required
from flask_restful import Resource, reqparse, marshal, marshal_with, fields, abort
from sqlalchemy.exc import IntegrityError, OperationalError
from werkzeug.security import generate_password_hash

from . import app, db
from .forms import AddUserForm, UpdateUserForm
from .models import User


@app.route('/add_user')
@jwt_required()
def add_user():
    form = AddUserForm()
    return render_template('add_user.html', title='Add User', form=form)


@app.route('/update_user/<string:name>')
@jwt_required()
def update_user(name):
    form = UpdateUserForm()
    user = abort_if_user_doesnt_exist(name)
    return render_template('update_user.html', title='Update User',
                           form=form, uid=user.id, name=name, role=user.role)


@app.route('/delete_user/<string:name>')
@jwt_required()
def delete_user(name):
    from flask_wtf import FlaskForm
    abort_if_user_doesnt_exist(name)
    form = FlaskForm()
    return render_template('delete_user.html', title='Delete User', form=form, name=name)


def abort_if_user_doesnt_exist(name):
    try:
        user = User.query.filter_by(name=name).first()
        if not user:
            abort(404, message="user {} doesn't exist".format(name))
        return user
    except OperationalError:
        abort(500, message='_mysql_exceptions.OperationalError')


user_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'password': fields.String,
}


class UserResource(Resource):
    method_decorators = {
        'get': [jwt_required()],
        'post': [jwt_required()],
        'delete': [jwt_required()],
        'put': [jwt_required()],
    }

    @marshal_with(user_fields)
    def get(self, name):
        user = abort_if_user_doesnt_exist(name)
        return user

    def delete(self, name):
        user = abort_if_user_doesnt_exist(name)
        db.session.delete(user)
        db.session.commit()
        print('delete ' + str(name))
        return 'delete ' + user.name + ' success', 200

    @marshal_with(user_fields)
    def put(self, name):
        # update data
        # see http://www.bjhee.com/flask-ext4.html
        parser = reqparse.RequestParser()
        parser.add_argument('name')
        parser.add_argument('password')
        args = parser.parse_args()
        try:
            user = User.query.filter_by(name=name).first()
        except OperationalError:
            return [], 500
        print(user)
        if not user:
            return [], 403
        user.password = args['password']
        print(user)
        db.session.add(user)
        db.session.commit()
        return user, 201

    def post(self, name):
        parser = reqparse.RequestParser()
        parser.add_argument('_method')
        args = parser.parse_args()
        method = args['_method']
        if method == 'put':
            return self.put(name)
        elif method == 'delete':
            return self.delete(name)
        return [], 403


class UsersResource(Resource):
    method_decorators = {
        'get': [jwt_required()],
        'post': [jwt_required()]
    }

    @marshal_with(user_fields)
    def get(self):
        return User.query.all()

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name')
        parser.add_argument('password')
        args = parser.parse_args()
        name = args['name']
        password = args['password']
        if name == 'admin':
            return {'error': 'user name cannot be admin'}, 400
        user = User(name=name, password=generate_password_hash(password))
        db.session.add(user)
        try:
            db.session.commit()
        except IntegrityError as e:
            print(e)
            return {'error': "Duplicate entry '" + user.name + "' for key 'name'"}, 201
        except OperationalError as e:
            print(e)
            return {'error': 'OperationalError'}, 201
        return marshal(user, user_fields), 201
