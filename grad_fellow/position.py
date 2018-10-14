# -*- coding:utf-8 -*-
from flask import render_template
from flask_login import login_required
from flask_restful import Resource, reqparse, marshal, marshal_with, fields, abort
from sqlalchemy.exc import IntegrityError, OperationalError

from . import db, app
from .forms import AddPositionForm, UpdatePositionForm
from .models import Position


@app.route('/add_position')
@login_required
def add_position():
    form = AddPositionForm()
    return render_template('add_position.html', title='Add Position', form=form)


@app.route('/update_position/<int:position_id>')
@login_required
def update_position(position_id):
    form = UpdatePositionForm()
    return render_template('update_position.html', title='Update Position', form=form, position_id=position_id)


@app.route('/delete_position/<int:position_id>')
@login_required
def delete_position(position_id):
    from flask_wtf import FlaskForm
    form = FlaskForm()
    return render_template('delete_position.html', title='Delete Position', form=form, position_id=position_id)


def abort_if_position_doesnt_exist(position_id):
    try:
        position = Position.query.filter_by(id=position_id).first()
        if not position:
            abort(404, message="position_id {} doesn't exist".format(position_id))
        return position
    except OperationalError:
        abort(500, message='_mysql_exceptions.OperationalError')


position_fields = {
    'id': fields.Integer,
    'name': fields.String,
}

parser = reqparse.RequestParser()
parser.add_argument('name')


class PositionResource(Resource):
    method_decorators = {
        'post': [login_required],
        'delete': [login_required],
        'put': [login_required],
    }

    @marshal_with(position_fields)
    def get(self, position_id):
        print('get ' + str(position_id))
        position = abort_if_position_doesnt_exist(position_id)
        return position

    def delete(self, position_id):
        position = abort_if_position_doesnt_exist(position_id)
        db.session.delete(position)
        db.session.commit()
        print('delete ' + str(position_id))
        return 'delete ' + position.name + ' success', 200

    @marshal_with(position_fields)
    def put(self, position_id):
        # update data
        # see http://www.bjhee.com/flask-ext4.html
        args = parser.parse_args()
        try:
            position = Position.query.filter_by(id=position_id).first()
        except OperationalError:
            return [], 500
        print(position)
        if not position:
            return [], 403
        position.name = args['name']
        print(position)
        db.session.add(position)
        db.session.commit()
        return position, 201

    def post(self, position_id):
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
    method_decorators = {
        'post': [login_required]
    }

    @marshal_with(position_fields)
    def get(self):
        return Position.query.order_by(Position.name).all()

    def post(self):
        args = parser.parse_args()
        position = Position(name=args['name'])
        db.session.add(position)
        try:
            db.session.commit()
        except IntegrityError as e:
            print(e)
            return {'error': "Duplicate entry '" + position.name + "' for key 'name'"}, 201
        except OperationalError as e:
            print(e)
            return {'error': 'OperationalError'}, 201
        return marshal(position, position_fields), 201
