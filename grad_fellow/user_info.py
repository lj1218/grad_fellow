# -*- coding:utf-8 -*-
from flask_login import login_required
from flask_restful import Resource, reqparse, marshal, marshal_with, fields, abort
from sqlalchemy.exc import IntegrityError, OperationalError

from . import db
from .models import UserInfo


def abort_if_user_info_doesnt_exist(name):
    try:
        user_info = UserInfo.query.filter_by(name=name).first()
        if not user_info:
            abort(404, message="user_info {} doesn't exist".format(name))
        return user_info
    except OperationalError:
        abort(500, message='_mysql_exceptions.OperationalError')


user_info_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'first_name': fields.String,
    'last_name': fields.String,
    'position': fields.String,
    'company': fields.String,
    'nationality': fields.String,
    'tobe_contacted': fields.String,
    'skills_have': fields.String,
    'skills_learned': fields.String,
    'skills_recommend': fields.String,
    'skills_roles_in_company': fields.String,
    'skills_tasks_auto': fields.String,
    'skills_tasks_collab': fields.String,
    'cc_competitiveness': fields.String,
    'cc_desc_by_colleagues': fields.String,
    'cc_working_approach': fields.String,
    'cc_relationship_with_colleague': fields.String,
    'cc_relationship_with_mgr': fields.String,
}


def get_parser():
    parser = reqparse.RequestParser()
    for argument in [f for f in user_info_fields.keys()][1:]:
        parser.add_argument(argument)
    return parser


def new_user_info(args):
    user_info = UserInfo(
        name=args['name'],
        first_name=args['first_name'],
        last_name=args['last_name'],
        position=args['position'],
        company=args['company'],
        nationality=args['nationality'],
        tobe_contacted=args['tobe_contacted'],
        skills_have=args['skills_have'],
        skills_learned=args['skills_learned'],
        skills_recommend=args['skills_recommend'],
        skills_roles_in_company=args['skills_roles_in_company'],
        skills_tasks_auto=args['skills_tasks_auto'],
        skills_tasks_collab=args['skills_tasks_collab'],
        cc_competitiveness=args['cc_competitiveness'],
        cc_desc_by_colleagues=args['cc_desc_by_colleagues'],
        cc_working_approach=args['cc_working_approach'],
        cc_relationship_with_colleague=args['cc_relationship_with_colleague'],
        cc_relationship_with_mgr=args['cc_relationship_with_mgr']
    )
    return user_info


class UserInfoResource(Resource):
    method_decorators = {
        'post': [login_required],
        'delete': [login_required],
        'put': [login_required],
    }

    @marshal_with(user_info_fields)
    def get(self, name):
        print('get ' + str(name))
        user_info = abort_if_user_info_doesnt_exist(name)
        return user_info

    def delete(self, name):
        user_info = abort_if_user_info_doesnt_exist(name)
        db.session.delete(user_info)
        db.session.commit()
        print('delete ' + str(name))
        return 'delete ' + user_info.name + ' success', 200

    @marshal_with(user_info_fields)
    def put(self, name):
        # update data
        # see http://www.bjhee.com/flask-ext4.html
        parser = UserInfosResource.get_parser()
        args = parser.parse_args()
        try:
            user_info = UserInfo.query.filter_by(name=name).first()
        except OperationalError:
            return [], 500
        print(user_info)
        if not user_info:
            return [], 403
        id_ = user_info.id
        user_info = new_user_info(args)
        user_info.id = id_
        print(user_info)
        db.session.add(user_info)
        db.session.commit()
        return user_info, 201

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


class UserInfosResource(Resource):
    method_decorators = {
        'post': [login_required]
    }

    @marshal_with(user_info_fields)
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('nationality', type=str)
        parser.add_argument('position', type=str)
        args = parser.parse_args()
        nationality = args['nationality']
        position = args['position']
        try:
            if nationality and position:
                user_info = UserInfo.query.filter_by(
                    nationality=nationality, position=position
                ).all()
            elif nationality:
                user_info = UserInfo.query.filter_by(
                    nationality=nationality
                ).all()
            elif position:
                user_info = UserInfo.query.filter_by(
                    position=position
                ).all()
            else:
                user_info = UserInfo.query.all()
        except OperationalError:
            return [], 500
        return user_info

    def post(self):
        args = get_parser().parse_args()
        user_info = new_user_info(args)
        db.session.add(user_info)
        try:
            db.session.commit()
        except IntegrityError as e:
            print(e)
            return {'error': "Duplicate entry '" + user_info.name + "' for key 'name'"}, 201
        except OperationalError as e:
            print(e)
            return {'error': 'OperationalError'}, 201
        return marshal(user_info, user_info_fields), 201
