# -*- coding:utf-8 -*-
"""Abort functions."""
from sqlalchemy.exc import OperationalError

from ..models import Administrator, Country, Position, User, UserInfo


def __abort_if_data_doesnt_exist(abort, model, field_name, field_val, by='id'):
    try:
        obj = None
        if by == 'id':
            obj = model.query.filter_by(id=field_val).first()
        elif by == 'name':
            obj = model.query.filter_by(name=field_val).first()
        if not obj:
            abort(404, message="{0} {1} doesn't exist".format(
                field_name, field_val))
        return obj
    except OperationalError:
        abort(500, message='_mysql_exceptions.OperationalError')


def abort_if_country_doesnt_exist(abort, country_id):
    """Abort if country doesn't exist."""
    return __abort_if_data_doesnt_exist(
        abort, Country, 'country_id', country_id
    )


def abort_if_position_doesnt_exist(abort, position_id):
    """Abort if position doesn't exist."""
    return __abort_if_data_doesnt_exist(
        abort, Position, 'position_id', position_id
    )


def abort_if_administrator_doesnt_exist(abort, name):
    """Abort if administrator doesn't exist."""
    return __abort_if_data_doesnt_exist(
        abort, Administrator, 'administrator', name, by='name'
    )


def abort_if_user_doesnt_exist(abort, name):
    """Abort if user doesn't exist."""
    return __abort_if_data_doesnt_exist(
        abort, User, 'user', name, by='name'
    )


def abort_if_user_info_doesnt_exist(abort, name):
    """Abort if user_info doesn't exist."""
    return __abort_if_data_doesnt_exist(
        abort, UserInfo, 'user_info', name, by='name'
    )
