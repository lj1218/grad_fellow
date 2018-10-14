# -*- coding:utf-8 -*-
from sqlalchemy.exc import OperationalError
from werkzeug.security import generate_password_hash, check_password_hash

from . import db
from .models import Administrator, User


def set_password(password):
    try:
        admin = Administrator.query.filter_by(name='admin').first()
    except OperationalError as e:
        print(e)
        return False

    password_hash = generate_password_hash(password)
    if not admin:
        admin = Administrator(name='admin', password=password_hash)
    else:
        admin.password = password_hash

    db.session.add(admin)
    try:
        db.session.commit()
    except OperationalError as e:
        print(e)
        return False
    print('set password to {} success'.format(password))
    return True


def verify_admin_password(user_name, password):
    try:
        user = Administrator.query.filter_by(name=user_name).first()
    except OperationalError as e:
        print(e)
        return False
    if not user:
        return False
    return check_password_hash(user.password, password)


def verify_user_password(user_name, password):
    try:
        user = User.query.filter_by(name=user_name).first()
    except OperationalError as e:
        print(e)
        return False
    if not user:
        return False
    return check_password_hash(user.password, password)
