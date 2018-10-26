# -*- coding:utf-8 -*-
"""RESTful resource: Administrator."""
from flask_jwt import jwt_required
from flask_restful import Resource, fields, marshal_with, reqparse
from sqlalchemy.exc import OperationalError
from werkzeug.security import generate_password_hash

from ..db import db
from ..models import Administrator

admin_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'password': fields.String,
}


class AdminResource(Resource):
    """Admin Resource."""

    method_decorators = {'put': [jwt_required()]}

    @marshal_with(admin_fields)
    def put(self, name):
        """Put method."""
        # Update data (see http://www.bjhee.com/flask-ext4.html)
        parser = reqparse.RequestParser()
        parser.add_argument('name')
        parser.add_argument('password')
        args = parser.parse_args()
        try:
            user = Administrator.query.filter_by(name=name).first()
        except OperationalError:
            return [], 500
        print(user)
        if not user:
            return [], 403
        user.password = generate_password_hash(args['password'])
        print(user)
        print('user:{0}, password:{1}'.format(user.name, user.password))
        db.session.add(user)
        db.session.commit()
        return user, 201
