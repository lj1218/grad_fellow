# -*- coding:utf-8 -*-
"""RESTful resource: UserInfo."""
from flask_jwt import current_identity, jwt_required
from flask_restful import (Resource, abort, fields, marshal, marshal_with,
                           reqparse)
from sqlalchemy.exc import IntegrityError, OperationalError

from ..common.abort import abort_if_user_info_doesnt_exist
from ..db import db
from ..models import UserInfo

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
    """Get parser."""
    parser = reqparse.RequestParser()
    for argument in [f for f in user_info_fields.keys() if f != 'id']:
        parser.add_argument(argument)
    return parser


class UserInfoResource(Resource):
    """UserInfo Resource."""

    method_decorators = {
        'get': [jwt_required()],
        'post': [jwt_required()],
        'delete': [jwt_required()],
        'put': [jwt_required()],
    }

    @marshal_with(user_info_fields)
    def get(self, name):
        """Get method."""
        user_info = abort_if_user_info_doesnt_exist(abort, name)
        return user_info

    def delete(self, name):
        """Delete method."""
        user_info = abort_if_user_info_doesnt_exist(abort, name)
        db.session.delete(user_info)
        db.session.commit()
        print('delete ' + str(name))
        return 'delete ' + user_info.name + ' success', 200

    @marshal_with(user_info_fields)
    def post(self, name):
        """Post method."""
        # Update data (see http://www.bjhee.com/flask-ext4.html)
        parser = UserInfosResource.get_parser()
        args = parser.parse_args()
        user = current_identity
        username = user.username
        print('UserInfoResource.put - username: ' + username)
        user_info = UserInfo.query.filter_by(name=username).first()
        if user_info is None:
            user_info = _new_user_info(username, args)
        else:
            _update_user_info(user_info, args)
        print(user_info)
        db.session.add(user_info)
        db.session.commit()
        return user_info, 201


class UserInfosResource(Resource):
    """UserInfos Resource."""

    method_decorators = {
        'post': [jwt_required()]
    }

    @marshal_with(user_info_fields)
    def get(self):
        """Get method."""
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
        """Post method."""
        args = get_parser().parse_args()
        user = current_identity
        username = user.username
        print('UserInfosResource.post - username: ' + username)
        user_info = UserInfo.query.filter_by(name=username).first()
        if user_info is None:
            user_info = _new_user_info(username, args)
        else:
            _update_user_info(user_info, args)
        try:
            db.session.add(user_info)
            db.session.commit()
        except IntegrityError as e:
            print(e)
            return {'error': "User info for '" + user_info.name +
                             "' already exists"}, 409
        except OperationalError as e:
            print(e)
            return {'error': 'OperationalError'}, 500
        return marshal(user_info, user_info_fields), 201


def _new_user_info(username, args):
    """Create UserInfo instance."""
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
        cc_relationship_with_colleague=args.get(
            'cc_relationship_with_colleague', ''),
        cc_relationship_with_mgr=args.get('cc_relationship_with_mgr', '')
    )
    return user_info


def _update_user_info(old, args):
    """Update old UserInfo instance with args."""
    new = _new_user_info(old.name, args)
    old.first_name = new.first_name
    old.last_name = new.last_name
    old.position = new.position
    old.company = new.company
    old.nationality = new.nationality
    old.tobe_contacted = new.tobe_contacted
    old.skills_have = new.skills_have
    old.skills_learned = new.skills_learned
    old.skills_recommend = new.skills_recommend
    old.skills_roles_in_company = new.skills_roles_in_company
    old.skills_tasks_auto = new.skills_tasks_auto
    old.skills_tasks_collab = new.skills_tasks_collab
    old.cc_competitiveness = new.cc_competitiveness
    old.cc_desc_by_colleagues = new.cc_desc_by_colleagues
    old.cc_working_approach = new.cc_working_approach
    old.cc_relationship_with_colleague = new.cc_relationship_with_colleague
    old.cc_relationship_with_mgr = new.cc_relationship_with_mgr
    return old
