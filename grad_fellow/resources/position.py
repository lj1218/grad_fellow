# -*- coding:utf-8 -*-
"""RESTful resource: Position."""
import logging

from flask_jwt import jwt_required
from flask_restful import (Resource, abort, fields, marshal, marshal_with,
                           reqparse)
from sqlalchemy.exc import IntegrityError, OperationalError

from ..common.abort import abort_if_position_doesnt_exist
from ..db import db
from ..models import Position

logger = logging.getLogger(__name__)

position_fields = {
    'id': fields.Integer,
    'name': fields.String,
}

parser = reqparse.RequestParser()
parser.add_argument('name')


class PositionResource(Resource):
    """Position Resource."""

    method_decorators = {
        'post': [jwt_required()],
        'delete': [jwt_required()],
        'put': [jwt_required()],
    }

    @marshal_with(position_fields)
    def get(self, position_id):
        """Get method."""
        position = abort_if_position_doesnt_exist(abort, position_id)
        return position

    def delete(self, position_id):
        """Delete method."""
        position = abort_if_position_doesnt_exist(abort, position_id)
        db.session.delete(position)
        db.session.commit()
        logger.info('delete ' + str(position_id))
        return {'msg': 'delete ' + position.name + ' success'}, 200

    def put(self, position_id):
        """Put method."""
        # Update data (see http://www.bjhee.com/flask-ext4.html)
        args = parser.parse_args()
        new_name = args['name']
        try:
            position = Position.query.filter_by(id=position_id).first()
        except OperationalError:
            return [], 500
        logger.debug(position)
        if not position:
            return [], 403
        position.name = new_name
        logger.debug(position)
        try:
            db.session.add(position)
            db.session.commit()
        except IntegrityError as e:
            logger.error(str(e))
            return {'error': "Position '" + new_name +
                             "' already exists"}, 409
        except OperationalError as e:
            logger.error(str(e))
            return {'error': 'OperationalError'}, 500

        return marshal(position, position_fields), 201

    def post(self, position_id):
        """Post method."""
        parser2 = reqparse.RequestParser()
        parser2.add_argument('_method')
        args = parser2.parse_args()
        method = args['_method']
        if method == 'put':
            return self.put(position_id)
        elif method == 'delete':
            return self.delete(position_id)
        return '', 403


class PositionsResource(Resource):
    """Positions Resource."""

    method_decorators = {
        'post': [jwt_required()]
    }

    @marshal_with(position_fields)
    def get(self):
        """Get method."""
        return Position.query.order_by(Position.name).all()

    def post(self):
        """Post method."""
        args = parser.parse_args()
        position = Position(name=args['name'])
        try:
            db.session.add(position)
            db.session.commit()
        except IntegrityError as e:
            logger.error(str(e))
            return {'error': "Position '" + position.name +
                             "' already exists"}, 409
        except OperationalError as e:
            logger.error(str(e))
            return {'error': 'OperationalError'}, 500
        return marshal(position, position_fields), 201
