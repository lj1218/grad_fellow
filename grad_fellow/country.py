# -*- coding:utf-8 -*-
from flask import render_template
from flask_login import login_required
from flask_restful import Resource, reqparse, marshal, marshal_with, fields, abort
from sqlalchemy.exc import IntegrityError, OperationalError

from . import db, app
from .forms import AddCountryForm, UpdateCountryForm
from .models import Country


@app.route('/add_country')
@login_required
def add_country():
    form = AddCountryForm()
    return render_template('add_country.html', title='Add Country', form=form)


@app.route('/update_country/<int:country_id>')
@login_required
def update_country(country_id):
    form = UpdateCountryForm()
    return render_template('update_country.html', title='Update Country', form=form, country_id=country_id)


@app.route('/delete_country/<int:country_id>')
@login_required
def delete_country(country_id):
    from flask_wtf import FlaskForm
    form = FlaskForm()
    return render_template('delete_country.html', title='Delete Country', form=form, country_id=country_id)


def abort_if_country_doesnt_exist(country_id):
    try:
        country = Country.query.filter_by(id=country_id).first()
        if not country:
            abort(404, message="country_id {} doesn't exist".format(country_id))
        return country
    except OperationalError:
        abort(500, message='_mysql_exceptions.OperationalError')


country_fields = {
    'id': fields.Integer,
    'name': fields.String,
}

parser = reqparse.RequestParser()
parser.add_argument('name')


class CountryResource(Resource):
    method_decorators = {
        'post': [login_required],
        'delete': [login_required],
        'put': [login_required],
    }

    @marshal_with(country_fields)
    def get(self, country_id):
        print('get ' + str(country_id))
        country = abort_if_country_doesnt_exist(country_id)
        return country

    def delete(self, country_id):
        country = abort_if_country_doesnt_exist(country_id)
        db.session.delete(country)
        db.session.commit()
        print('delete ' + str(country_id))
        return 'delete ' + country.name + ' success', 200

    @marshal_with(country_fields)
    def put(self, country_id):
        # update data
        # see http://www.bjhee.com/flask-ext4.html
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
    method_decorators = {
        'post': [login_required]
    }

    @marshal_with(country_fields)
    def get(self):
        return Country.query.order_by(Country.name).all()

    def post(self):
        args = parser.parse_args()
        country = Country(name=args['name'])
        db.session.add(country)
        try:
            db.session.commit()
        except IntegrityError as e:
            print(e)
            return {'error': "Duplicate entry '" + country.name + "' for key 'name'"}, 201
        except OperationalError as e:
            print(e)
            return {'error': 'OperationalError'}, 201
        return marshal(country, country_fields), 201
