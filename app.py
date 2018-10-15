# -*- coding:utf-8 -*-
from flask import redirect, url_for

from grad_fellow.user import UserResource, UsersResource
from grad_fellow.country import CountryResource, CountriesResource
from grad_fellow.position import PositionResource, PositionsResource
from grad_fellow.user_info import UserInfoResource, UserInfosResource
from flask_jwt import jwt_required

from grad_fellow import app, api
from grad_fellow.util import save_pid


@app.route('/logout')
@jwt_required()
def logout():
    # logout_user()
    return redirect(url_for('login'))


api.add_resource(UsersResource, '/user')
api.add_resource(UserResource, '/user/<name>')

api.add_resource(CountriesResource, '/country')
api.add_resource(CountryResource, '/country/<country_id>')

api.add_resource(PositionsResource, '/position')
api.add_resource(PositionResource, '/position/<position_id>')

api.add_resource(UserInfosResource, '/userinfo')
api.add_resource(UserInfoResource, '/userinfo/<name>')


if __name__ == '__main__':
    save_pid()
    app.run(host='0.0.0.0')
