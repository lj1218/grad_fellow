# -*- coding:utf-8 -*-
from flask_jwt import jwt_required, current_identity
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
    # 'name': fields.String,
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
    for argument in [f for f in user_info_fields.keys() if f != 'id']:
        parser.add_argument(argument)
    return parser


def new_user_info(username, args):
    print('type(args): ' + str(type(args)))
    print(str(args))
    if args['tobe_contacted'] == 'True':
        tobe_contacted = True
    else:
        tobe_contacted = False
    user_info = UserInfo(
        name=username,
        first_name=args.get('first_name', ''),
        last_name=args.get('last_name', ''),
        position=args.get('position', ''),
        company=args.get('company', ''),
        nationality=args.get('nationality', ''),
        tobe_contacted=tobe_contacted,
        skills_have=args.get('skills_have', ''),
        skills_learned=args.get('skills_learned', ''),
        skills_recommend=args.get('skills_recommend', ''),
        skills_roles_in_company=args.get('skills_roles_in_company', ''),
        skills_tasks_auto=args.get('skills_tasks_auto', ''),
        skills_tasks_collab=args.get('skills_tasks_collab', ''),
        cc_competitiveness=args.get('cc_competitiveness', ''),
        cc_desc_by_colleagues=args.get('cc_desc_by_colleagues', ''),
        cc_working_approach=args.get('cc_working_approach', ''),
        cc_relationship_with_colleague=args.get('cc_relationship_with_colleague', ''),
        cc_relationship_with_mgr=args.get('cc_relationship_with_mgr', '')
    )
    return user_info


def update_user_info(user_info, args):
    _new_user_info = new_user_info(user_info.name, args)
    user_info.first_name = _new_user_info.first_name
    user_info.last_name = _new_user_info.last_name
    user_info.position = _new_user_info.position
    user_info.company = _new_user_info.company
    user_info.nationality = _new_user_info.nationality
    user_info.tobe_contacted = _new_user_info.tobe_contacted
    user_info.skills_have = _new_user_info.skills_have
    user_info.skills_learned = _new_user_info.skills_learned
    user_info.skills_recommend = _new_user_info.skills_recommend
    user_info.skills_roles_in_company = _new_user_info.skills_roles_in_company
    user_info.skills_tasks_auto = _new_user_info.skills_tasks_auto
    user_info.skills_tasks_collab = _new_user_info.skills_tasks_collab
    user_info.cc_competitiveness = _new_user_info.cc_competitiveness
    user_info.cc_desc_by_colleagues = _new_user_info.cc_desc_by_colleagues
    user_info.cc_working_approach = _new_user_info.cc_working_approach
    user_info.cc_relationship_with_colleague = _new_user_info.cc_relationship_with_colleague
    user_info.cc_relationship_with_mgr = _new_user_info.cc_relationship_with_mgr
    return user_info


class UserInfoResource(Resource):
    method_decorators = {
        'get': [jwt_required()],
        'post': [jwt_required()],
        'delete': [jwt_required()],
        'put': [jwt_required()],
    }

    @marshal_with(user_info_fields)
    def get(self, name):
        user_info = abort_if_user_info_doesnt_exist(name)
        return user_info

    def delete(self, name):
        user_info = abort_if_user_info_doesnt_exist(name)
        db.session.delete(user_info)
        db.session.commit()
        print('delete ' + str(name))
        return 'delete ' + user_info.name + ' success', 200

    @marshal_with(user_info_fields)
    def post(self, name):
        # update data
        # see http://www.bjhee.com/flask-ext4.html
        parser = UserInfosResource.get_parser()
        args = parser.parse_args()
        user = current_identity
        username = user.username
        print('UserInfoResource.put - username: ' + username)
        user_info = UserInfo.query.filter_by(name=username).first()
        if user_info is None:
            user_info = new_user_info(username, args)
        else:
            update_user_info(user_info, args)
        print(user_info)
        db.session.add(user_info)
        db.session.commit()
        return user_info, 201


class UserInfosResource(Resource):
    method_decorators = {
        'post': [jwt_required()]
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
        user = current_identity
        username = user.username
        print('UserInfosResource.post - username: ' + username)
        user_info = UserInfo.query.filter_by(name=username).first()
        if user_info is None:
            user_info = new_user_info(username, args)
        else:
            update_user_info(user_info, args)
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
