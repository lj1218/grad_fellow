# -*- coding:utf-8 -*-
"""RESTful resource: Administrator."""
import logging

from flask_jwt import jwt_required
from flask_restful import Resource, abort, fields, marshal_with, reqparse
from sqlalchemy.exc import OperationalError
from werkzeug.security import generate_password_hash

from ..common.abort import abort_if_administrator_doesnt_exist
from ..db import db
from ..models import Administrator

logger = logging.getLogger(__name__)

admin_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'password': fields.String,
}


class AdminResource(Resource):
    """Admin Resource."""

    method_decorators = {
        'delete': [jwt_required()],
        'put': [jwt_required()]
    }

    def delete(self, name):
        """Delete method."""
        administrator = abort_if_administrator_doesnt_exist(abort, name)
        db.session.delete(administrator)
        db.session.commit()
        logger.info('delete ' + str(administrator))
        return {'msg': 'delete ' + administrator.name + ' success'}, 200

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
        logger.debug(user)
        # jwt guarantees user is not None
        user.password = generate_password_hash(args['password'])
        logger.debug(user)
        logger.debug('user:{0}, password:{1}'.format(user.name, user.password))
        db.session.add(user)
        db.session.commit()
        return user, 201
