# -*- coding:utf-8 -*-
"""RESTful resource: Country."""
from flask_jwt import jwt_required
from flask_restful import (Resource, abort, fields, marshal, marshal_with,
                           reqparse)
from sqlalchemy.exc import IntegrityError, OperationalError

from ..common.abort import abort_if_country_doesnt_exist
from ..db import db
from ..models import Country

country_fields = {
    'id': fields.Integer,
    'name': fields.String,
}

parser = reqparse.RequestParser()
parser.add_argument('name')


class CountryResource(Resource):
    """Country Resource."""

    method_decorators = {
        'post': [jwt_required()],
        'delete': [jwt_required()],
        'put': [jwt_required()],
    }

    @marshal_with(country_fields)
    def get(self, country_id):
        """Get method."""
        country = abort_if_country_doesnt_exist(abort, country_id)
        return country

    def delete(self, country_id):
        """Delete method."""
        country = abort_if_country_doesnt_exist(abort, country_id)
        db.session.delete(country)
        db.session.commit()
        print('delete ' + str(country_id))
        return 'delete ' + country.name + ' success', 200

    @marshal_with(country_fields)
    def put(self, country_id):
        """Put method."""
        # Update data (see http://www.bjhee.com/flask-ext4.html)
        args = parser.parse_args()
        try:
            country = Country.query.filter_by(id=country_id).first()
        except OperationalError:
            return [], 500
        print(country)
        if not country:
            return [], 403
        country.name = args['name']
        print(country)
        db.session.add(country)
        db.session.commit()
        return country, 201

    def post(self, country_id):
        """Post method."""
        parser2 = reqparse.RequestParser()
        parser2.add_argument('_method')
        args = parser2.parse_args()
        method = args['_method']
        if method == 'put':
            return self.put(country_id)
        elif method == 'delete':
            return self.delete(country_id)
        return [], 403


class CountriesResource(Resource):
    """Countries Resource."""

    method_decorators = {
        'post': [jwt_required()]
    }

    @marshal_with(country_fields)
    def get(self):
        """Get method."""
        return Country.query.all()

    def post(self):
        """Post method."""
        args = parser.parse_args()
        country = Country(name=args['name'])
        db.session.add(country)
        try:
            db.session.commit()
        except IntegrityError as e:
            print(e)
            return {'error': "Duplicate entry '" + country.name +
                             "' for key 'name'"}, 201
        except OperationalError as e:
            print(e)
            return {'error': 'OperationalError'}, 201
        return marshal(country, country_fields), 201
