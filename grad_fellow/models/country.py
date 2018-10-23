# -*- coding:utf-8 -*-
"""Model: Country."""
from ..db import db


class Country(db.Model):
    """Country."""

    # 国家id
    id = db.Column(db.Integer, primary_key=True)
    # 国家名称
    name = db.Column(db.String(100), unique=True, nullable=False)

    def __repr__(self):
        """Provide usable string representations of itself."""
        return '<Country %r>' % self.name
