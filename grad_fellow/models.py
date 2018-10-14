# -*- coding:utf-8 -*-
# models.py
from flask_login import UserMixin
from sqlalchemy.exc import OperationalError
from grad_fellow.acl import check_access_permission
from . import db


class User4Auth(UserMixin):

    def __init__(self, username):
        self.username = username
        self.id = self.get_id()

    def get_id(self):
        user = None
        if self.username == 'admin':
            try:
                user = Administrator.query.filter_by(name=self.username).first()
            except OperationalError as e:
                print(e)
        else:
            try:
                user = User.query.filter_by(name=self.username).first()
            except OperationalError as e:
                print(e)
        password = user and user.password
        return [self.username, password]

    def verify_password(self, password):
        from grad_fellow.admin import verify_user_password, verify_admin_password
        if self.username == 'admin':
            return verify_admin_password(self.username, password)
        else:
            return verify_user_password(self.username, password)

    @staticmethod
    def get(user_id):
        """try to return user_id corresponding User object.
        This method is used by load_user callback function
        """
        username = user_id[0]
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


class Administrator(db.Model):

    # 用户id
    id = db.Column(db.Integer, primary_key=True)
    # 用户名，用于登录系统
    name = db.Column(db.String(100), unique=True, nullable=False)
    # 密码(加密)
    password = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return '<Administrator %r>' % self.name


class User(db.Model):

    # 用户id
    id = db.Column(db.Integer, primary_key=True)
    # 用户名，用于登录系统
    name = db.Column(db.String(100), unique=True, nullable=False)
    # 密码(加密)
    password = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.name


class Country(db.Model):
    # 国家id
    id = db.Column(db.Integer, primary_key=True)
    # 国家名称
    name = db.Column(db.String(100), unique=True, nullable=False)

    def __repr__(self):
        return '<Country %r>' % self.name


class Position(db.Model):
    # 职位id
    id = db.Column(db.Integer, primary_key=True)
    # 职位名称
    name = db.Column(db.String(100), unique=True, nullable=False)

    def __repr__(self):
        return '<Position %r>' % self.name


class UserInfo(db.Model):
    # 自增id
    id = db.Column(db.Integer, primary_key=True)
    # 用户名，用于登录系统（外键 user.name）
    name = db.Column(db.String(100), db.ForeignKey('user.name'), unique=True, nullable=False)

    # -------------------------- Basic Info ----------------------
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    # 当前职位
    position = db.Column(db.String(100), nullable=False)
    # 当前就职公司
    company = db.Column(db.String(100), nullable=False)
    # 国籍
    nationality = db.Column(db.String(100), nullable=False)
    # 是否愿意被联系
    tobe_contacted = db.Column(db.Boolean, nullable=False)

    # -------------------------- Skills --------------------------
    # 拥有的技能
    skills_have = db.Column(db.Text, nullable=False)
    # 学习到的技能
    skills_learned = db.Column(db.Text, nullable=False)
    # 推荐的技能
    skills_recommend = db.Column(db.Text, nullable=False)
    # 工作中需要沟通的角色
    skills_roles_in_company = db.Column(db.Text, nullable=False)
    # 自主完成的任务
    skills_tasks_auto = db.Column(db.Text, nullable=False)
    # 协作完成的任务
    skills_tasks_collab = db.Column(db.Text, nullable=False)

    # -------------------------- Company Culture -----------------
    cc_competitiveness = db.Column(db.Text, nullable=False)
    cc_desc_by_colleagues = db.Column(db.Text, nullable=False)
    cc_working_approach = db.Column(db.Text, nullable=False)
    cc_relationship_with_colleague = db.Column(db.Text, nullable=False)
    cc_relationship_with_mgr = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return '<UserInfo name=%r>' % self.name
