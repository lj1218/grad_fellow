# -*- coding:utf-8 -*-
"""RESTful resource: User."""
import logging

from flask_jwt import jwt_required
from flask_restful import (Resource, abort, fields, marshal, marshal_with,
                           reqparse)
from sqlalchemy.exc import IntegrityError, OperationalError
from werkzeug.security import generate_password_hash

from ..common.abort import abort_if_user_doesnt_exist
from ..db import db
from ..models import User

logger = logging.getLogger(__name__)

user_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'password': fields.String,
}


class UserResource(Resource):
    """User Resource."""

    method_decorators = {
        'get': [jwt_required()],
        'post': [jwt_required()],
        'delete': [jwt_required()],
        'put': [jwt_required()],
    }

    @marshal_with(user_fields)
    def get(self, name):
        """Get method."""
        user = abort_if_user_doesnt_exist(abort, name)
        return user

    def delete(self, name):
        """Delete method."""
        user = abort_if_user_doesnt_exist(abort, name)
        try:
            db.session.delete(user)
            db.session.commit()
        except IntegrityError as e:
            logger.error(str(e))
            return {'error': "Cannot delete: a foreign key" +
                             " constraint fails"}, 409
        logger.info('delete ' + str(name))
        return {'msg': 'delete ' + user.name + ' success'}, 200

    @marshal_with(user_fields)
    def put(self, name):
        """Put method."""
        # Update data (see http://www.bjhee.com/flask-ext4.html)
        parser = reqparse.RequestParser()
        parser.add_argument('password')
        args = parser.parse_args()
        try:
            user = User.query.filter_by(name=name).first()
        except OperationalError:
            return [], 500
        logger.debug(user)
        if not user:
            return [], 403
        user.password = generate_password_hash(args['password'])
        logger.debug(user)
        db.session.add(user)
        db.session.commit()
        return user, 201

    def post(self, name):
        """Post method."""
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
    """Users Resource."""

    method_decorators = {
        'get': [jwt_required()],
        'post': [jwt_required()]
    }

    @marshal_with(user_fields)
    def get(self):
        """Get method."""
        return User.query.all()

    def post(self):
        """Post method."""
        parser = reqparse.RequestParser()
        parser.add_argument('name')
        parser.add_argument('password')
        args = parser.parse_args()
        name = args['name']
        password = args['password']
        if name == 'admin':
            return {'error': 'user name cannot be admin'}, 409
        user = User(name=name, password=generate_password_hash(password))
        try:
            db.session.add(user)
            db.session.commit()
        except IntegrityError as e:
            logger.error(str(e))
            return {'error': "User '" + user.name +
                             "' already exists"}, 409
        except OperationalError as e:
            logger.error(str(e))
            return {'error': 'OperationalError'}, 500
        return marshal(user, user_fields), 201
