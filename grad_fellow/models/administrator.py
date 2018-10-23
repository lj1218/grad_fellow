# -*- coding:utf-8 -*-
"""Model: Administrator."""
from ..db import db


class Administrator(db.Model):
    """Administrator."""

    # 用户id
    id = db.Column(db.Integer, primary_key=True)
    # 用户名，用于登录系统
    name = db.Column(db.String(100), unique=True, nullable=False)
    # 密码(加密)
    password = db.Column(db.Text, nullable=False)

    def __repr__(self):
        """Provide usable string representations of itself."""
        return '<Administrator %r>' % self.name
