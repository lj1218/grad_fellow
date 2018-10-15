# -*- coding:utf-8 -*-
import os
from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt import JWT


def authenticate(username, password):
    from .models import User4Auth
    print('authenticate: {}:{}'.format(username, password))
    user = User4Auth(username)
    if not user.verify_password(password):
        print('fail')
        return
    return user


def identity(payload):
    from grad_fellow.acl import check_access_permission
    from sqlalchemy.exc import OperationalError
    from .models import User, User4Auth, Administrator

    user_id = payload['identity']
    username = user_id[0]
    print('username: ' + username)
    password = user_id[1]
    if not check_access_permission(username):
        return None
    if not password:
        return None
    user = None
    if username == 'admin':
        try:
            user = Administrator.query.filter_by(name=username).first()
        except OperationalError as e:
            print(e)
    else:
        try:
            user = User.query.filter_by(name=username).first()
        except OperationalError as e:
            print(e)
    if user and password == user.password:
        return User4Auth(username)
    return None


app = Flask(__name__)
app.debug = True
CORS(app, supports_credentials=True)  # 跨域问题

# https://flask-restful.readthedocs.io/en/latest/quickstart.html#full-example
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:123456@localhost:3306/grad_fellow_testdb'
# 设置这一项是每次请求结束后都会自动提交数据库中的变动
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = 'super-secret'
app.config['JWT_AUTH_URL_RULE'] = '/login'
db = SQLAlchemy(app)

app.secret_key = os.urandom(24)

jwt = JWT(app, authenticate, identity)
