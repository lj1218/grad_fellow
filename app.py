# -*- coding:utf-8 -*-
from flask import render_template, request, redirect, url_for, abort
from flask_wtf import CSRFProtect

from grad_fellow.user import UserResource, UsersResource
from grad_fellow.country import CountryResource, CountriesResource
from grad_fellow.position import PositionResource, PositionsResource
from grad_fellow.user_info import UserInfoResource, UserInfosResource
from grad_fellow.forms import LoginForm
from grad_fellow.models import User4Auth
from flask_login import login_user, login_required
from flask_login import LoginManager, current_user
from flask_login import logout_user

from grad_fellow import app, api
from grad_fellow.util import is_safe_url, save_pid

# use login manager to manage session
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'login'
login_manager.init_app(app=app)


# 这个callback函数用于reload User object，根据session中存储的user_id
@login_manager.user_loader
def load_user(user_id):
    print('user_id:' + str(user_id))
    return User4Auth.get(user_id)


# csrf protection
csrf = CSRFProtect()
csrf.init_app(app)


@app.route('/')
@app.route('/main')
@login_required
def main():
    return 'Hello ' + current_user.username + '!'


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = request.form.get('username', None)
        password = request.form.get('password', None)
        remember_me = request.form.get('remember_me', False)
        user = User4Auth(username=username)
        if user.verify_password(password):
            print(login_user(user, remember=remember_me))
            next_page = request.args.get('next')
            # is_safe_url should check if the url is safe for redirects.
            # See http://flask.pocoo.org/snippets/62/ for an example.
            if not is_safe_url(next_page):
                return abort(400)
            return redirect(next_page or url_for('main'))
    return render_template('login.html', title="Sign In",
                           form=form, path='/login')


@app.route('/admin', methods=['GET', 'POST'])
def login_admin():
    form = LoginForm()
    if form.validate_on_submit():
        username = request.form.get('username', None)
        password = request.form.get('password', None)
        remember_me = request.form.get('remember_me', False)
        user = User4Auth(username=username)
        if user.verify_password(password):
            print(login_user(user, remember=remember_me))
            print(url_for('add_user'))
            return redirect(url_for('add_user'))
        else:
            print('fail')
            return 'account or password error'
    return render_template('login.html', title="Sign In",
                           form=form, path='/admin')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


api.add_resource(UsersResource, '/user', '/user/')
api.add_resource(UserResource, '/user/<name>')

api.add_resource(CountriesResource, '/country', '/country/')
api.add_resource(CountryResource, '/country/<country_id>')

api.add_resource(PositionsResource, '/position', '/position/')
api.add_resource(PositionResource, '/position/<position_id>')

api.add_resource(UserInfosResource, '/userinfo', '/userinfo/')
api.add_resource(UserInfoResource, '/userinfo/<name>')


if __name__ == '__main__':
    save_pid()
    app.run(host='0.0.0.0')
