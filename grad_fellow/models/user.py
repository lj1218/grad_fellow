# -*- coding:utf-8 -*-
"""Model: User."""
from ..db import db


class User(db.Model):
    """User."""

    # 用户id
    id = db.Column(db.Integer, primary_key=True)
    # 用户名(用于系统登录)
    name = db.Column(db.String(100), unique=True, nullable=False)
    # 密码(加密)
    password = db.Column(db.Text, nullable=False)

    def __repr__(self):
        """Provide usable string representations of itself."""
        return '<User %r>' % self.name
