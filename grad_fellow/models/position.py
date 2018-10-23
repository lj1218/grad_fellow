# -*- coding:utf-8 -*-
"""Model: Position."""
from ..db import db


class Position(db.Model):
    """Position."""

    # 职位id
    id = db.Column(db.Integer, primary_key=True)
    # 职位名称
    name = db.Column(db.String(100), unique=True, nullable=False)

    def __repr__(self):
        """Provide usable string representations of itself."""
        return '<Position %r>' % self.name
