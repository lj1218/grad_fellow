"""Configuration."""
import os

db_username = 'root'
db_password = '123456'
db_name = 'grad_fellow_testdb'

SECRET_KEY = os.urandom(24)
SQLALCHEMY_ECHO = False
SQLALCHEMY_DATABASE_URI = 'mysql://{0}:{1}@localhost:3306/{2}'.format(
    db_username, db_password, db_name)
