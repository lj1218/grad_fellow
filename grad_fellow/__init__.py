# -*- coding:utf-8 -*-
"""Grad fellow package."""
import os

from datetime import timedelta
from flask import Blueprint, Flask
from flask_cors import CORS
from flask_restful import Api

from . import auth, db
from .admin import passwd
from .common.util import save_pid
from .resources.administrator import AdminResource
from .resources.country import CountriesResource, CountryResource
from .resources.position import PositionResource, PositionsResource
from .resources.user import UserResource, UsersResource
from .resources.user_info import UserInfoResource, UserInfosResource

__version__ = '1.0.1'


def create_app(test_config=None):
    """Create and configure the app."""
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY='dev',
        # SECRET_KEY=os.urandom(24),

        SQLALCHEMY_DATABASE_URI=__get_default_db_uri(),

        # track modifications of objects and emit signals
        SQLALCHEMY_TRACK_MODIFICATIONS=True,

        # # log all the statements issued to stderr
        # SQLALCHEMY_ECHO=True,

        JWT_AUTH_URL_RULE='/login',

        JWT_EXPIRATION_DELTA=timedelta(seconds=1800),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    app.debug = True

    # support cross origin resource sharing
    CORS(app, supports_credentials=True)

    __init_flask_restful(app)

    __register_blueprint(app)

    db.init_app(app)

    auth.init_app(app)

    passwd.init_app(app)

    save_pid()

    return app


def __get_default_db_uri():
    db_username = 'root'
    db_password = '123456'
    db_port = 3306
    db_name = 'grad_fellow_testdb'
    return 'mysql://{0}:{1}@localhost:{2}/{3}'.format(
        db_username, db_password, db_port, db_name
    )


def __init_flask_restful(app):
    # api_bp = Blueprint('api', __name__, url_prefix='/api')
    api_bp = Blueprint('api', __name__)
    api = Api(api_bp)
    app.register_blueprint(api_bp)
    api.add_resource(AdminResource, '/administrator/<name>')
    api.add_resource(UsersResource, '/user')
    api.add_resource(UserResource, '/user/<name>')
    api.add_resource(CountriesResource, '/country')
    api.add_resource(CountryResource, '/country/<country_id>')
    api.add_resource(PositionsResource, '/position')
    api.add_resource(PositionResource, '/position/<position_id>')
    api.add_resource(UserInfosResource, '/userinfo')
    api.add_resource(UserInfoResource, '/userinfo/<name>')


def __register_blueprint(app):
    """Apply blueprints to the app."""
    from .admin.webconsole import index
    from .admin.webconsole import auth
    from .admin.webconsole import country
    from .admin.webconsole import position
    from .admin.webconsole import user
    from .admin.webconsole import administrator
    app.register_blueprint(index.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(country.bp)
    app.register_blueprint(position.bp)
    app.register_blueprint(user.bp)
    app.register_blueprint(administrator.bp)
    app.add_url_rule('/', endpoint='index')
