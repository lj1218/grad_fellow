# -*- coding:utf-8 -*-
"""Configuration for test."""
import json

import pytest
from werkzeug.security import generate_password_hash

from grad_fellow import create_app
from grad_fellow.db import clear_db, db, init_db
from grad_fellow.logger import logger
from grad_fellow.models import Administrator, Country, Position, User, UserInfo

db_username = 'root'
db_password = '123456'
db_name = 'grad_fellow_testdb_tests'
SQLALCHEMY_DATABASE_URI = 'mysql://{0}:{1}@localhost:3306/{2}'.format(
    db_username, db_password, db_name)


@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    # create the app with common test config
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': SQLALCHEMY_DATABASE_URI,
        'LOGGER_ROTATING_FILE_CONF': None,
    })

    # create the database and load test data
    with app.app_context():
        init_db()
        init_data(db_data4test())

    yield app

    # clear database
    with app.app_context():
        clear_db()


@pytest.fixture
def client(app):
    """Get a test client for the app."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """Get a test runner for the app's Click commands."""
    return app.test_cli_runner()


class AuthActions(object):
    """Auth actions."""

    def __init__(self, client):
        """Init."""
        self._client = client

    def login(self, username, password):
        """Login web console."""
        return self._client.post(
            '/auth/login',
            content_type='application/json',
            data=json.dumps({'username': username, 'password': password})
        )

    def login_as_admin(self):
        """Login as admin."""
        response = self.login('admin', '123')
        assert response.status_code == 200
        return response

    def get(self, url):
        """Get method."""
        return self._client.get(url)

    def logout(self):
        """Logout."""
        return self._client.get('/auth/logout')


@pytest.fixture
def auth(client):
    """Get an AuthActions object."""
    return AuthActions(client)


class JwtAuthActions(object):
    """JWT Auth actions."""

    def __init__(self, client):
        """Init."""
        self._client = client
        self._access_token = None

    def login(self, username, password):
        """Login jwt."""
        response = self._client.post(
            '/login',
            content_type='application/json',
            data=json.dumps({'username': username, 'password': password})
        )
        if response.status_code == 200:
            self._access_token = json.loads(response.data).get('access_token')
        return response

    def login_as_admin(self):
        """Login as admin."""
        response = self.login('admin', '123')
        assert response.status_code == 200
        return response

    def get(self, url):
        """Get method."""
        return self._client.get(
            url,
            headers={'Authorization': 'JWT ' + str(self._access_token)}
        )

    def put(self, url, data):
        """Put method."""
        return self._client.put(
            url,
            headers={'Authorization': 'JWT ' + str(self._access_token)},
            content_type='application/json',
            data=json.dumps(data)
        )

    def post(self, url, data):
        """Post method."""
        return self._client.post(
            url,
            headers={'Authorization': 'JWT ' + str(self._access_token)},
            content_type='application/json',
            data=json.dumps(data)
        )

    def delete(self, url):
        """Delete method."""
        return self._client.delete(
            url,
            headers={'Authorization': 'JWT ' + str(self._access_token)},
            content_type='application/json'
        )

    def logout(self):
        """Logout."""
        pass


@pytest.fixture
def jwt_auth(client):
    """Get an JwtAuthActions object."""
    return JwtAuthActions(client)


def db_add_and_commit(db_, model):
    """Add and commit model to db."""
    from sqlalchemy.exc import OperationalError
    try:
        db_.session.add(model)
        db_.session.commit()
    except OperationalError as e:
        logger.error(str(e))
        exit(1)


def init_data(db_data):
    """Init test data."""
    init_data_for_admin(db_data)
    init_data_for_countries(db_data)
    init_data_for_positions(db_data)
    init_data_for_users(db_data)
    init_data_for_user_infos(db_data)


def init_data_for_admin(db_data):
    """Init test data for administrator."""
    administrators = db_data.get('administrator')
    if administrators is not None:
        rows = administrators.get('data')
        for row in rows:
            administrator = Administrator(
                name=row[0], password=generate_password_hash(row[1]))
            db_add_and_commit(db, administrator)


def init_data_for_countries(db_data):
    """Init test data for countries."""
    countries = db_data.get('country')
    if countries is not None:
        rows = countries.get('data')
        for row in rows:
            country = Country(name=row)
            db_add_and_commit(db, country)


def init_data_for_positions(db_data):
    """Init test data for positions."""
    positions = db_data.get('position')
    if positions is not None:
        rows = positions.get('data')
        for row in rows:
            position = Position(name=row)
            db_add_and_commit(db, position)


def init_data_for_users(db_data):
    """Init test data for users."""
    users = db_data.get('user')
    if users is not None:
        rows = users.get('data')
        for row in rows:
            user = User(name=row[0], password=generate_password_hash(row[1]))
            db_add_and_commit(db, user)


def init_data_for_user_infos(db_data):
    """Init test data user_infos."""
    user_infos = db_data.get('user_info')
    if user_infos is not None:
        rows = user_infos.get('data')
        for row in rows:
            user_info = UserInfo(
                name=row[0], first_name=row[1], last_name=row[2],
                position=row[3], company=row[4], nationality=row[5],
                tobe_contacted=row[6], skills_have=row[7],
                skills_learned=row[8]
            )
            db_add_and_commit(db, user_info)


def db_data4test():
    """Get data for test."""
    administrators = {
        'field': ['name', 'password'],
        'data': [
            ('admin', '123'),
        ]
    }

    countries = {
        'field': 'name',
        'data': [
            'China',
            'India'
        ]
    }

    positions = {
        'field': 'name',
        'data': [
            'Software EngineerSystem Analyst',
            'Business Analyst',
            'Technical support',
            'Network Engineer',
            'Technical Consultant',
            'Web Developer',
            'Software Test'
        ]
    }

    users = {
        'field': ['name', 'password'],
        'data': [
            ('test', '123456'),
            ('test2', '123456'),
            ('test3', '123456')
        ]
    }

    user_infos = {
        'field': [
            'name', 'first_name', 'last_name', 'position', 'company',
            'nationality', 'tobe_contacted', 'skills_have', 'skills_learned'
        ],
        'data': [
            (
                'test', 'Huang', 'Xiao', 'Business Analyst',
                'Global Consulting Services', 'China', 1,
                '3months Python Subject',
                'Advanced Python through on-job training'
            ),
            (
                'test2', 'Yong', 'Wu', 'Business Analyst',
                'REA', 'China', 0,
                '3 months Datawarehousing',
                'Project management skill'
            ),
        ]
    }

    return {
        'administrator': administrators,
        'country': countries,
        'position': positions,
        'user': users,
        'user_info': user_infos
    }

# https://click.palletsprojects.com/en/7.x/testing/
