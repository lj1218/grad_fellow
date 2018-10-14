# -*- coding:utf-8 -*-
import os
from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
CORS(app, supports_credentials=True)  # 跨域问题

# https://flask-restful.readthedocs.io/en/latest/quickstart.html#full-example
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:123456@localhost:3306/grad_fellow_testdb'
# 设置这一项是每次请求结束后都会自动提交数据库中的变动
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

app.secret_key = os.urandom(24)
