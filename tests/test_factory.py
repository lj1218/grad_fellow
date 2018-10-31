# -*- coding:utf-8 -*-
"""Test app config."""
from grad_fellow import create_app

db_username = 'root'
db_password = '123456'
db_name = 'test'
SQLALCHEMY_DATABASE_URI = 'mysql://{0}:{1}@localhost:3306/{2}'.format(
    db_username, db_password, db_name)


def test_config():
    """Test create_app without passing test config."""
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing
    assert create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': SQLALCHEMY_DATABASE_URI,
    }).config['SQLALCHEMY_DATABASE_URI'] == SQLALCHEMY_DATABASE_URI
