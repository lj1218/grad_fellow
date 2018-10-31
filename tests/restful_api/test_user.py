# -*- coding:utf-8 -*-
"""Test user."""
import json

import pytest


def test_unknown_method(client, jwt_auth):
    """Test unknown method xx."""
    jwt_auth.login_as_admin()
    response = jwt_auth.post('/user/test', {'_method': 'xx'})
    assert response.status_code == 403


@pytest.mark.parametrize(
    ('username', 'status_code', 'msgs'),
    (
            # get all users
            (None, 200, ['test', 'test2']),

            # username not exists
            ('test4', 404, None),

            # username exists
            ('test', 200, ['test']),
    )
)
def test_get_method(jwt_auth, username, status_code, msgs):
    """Test method 'GET'."""
    jwt_auth.login_as_admin()
    url = '/user' if username is None else '/user/' + username
    response = jwt_auth.get(url)
    assert response.status_code == status_code
    if msgs:
        for msg in msgs:
            assert msg in str(json.loads(response.data))


@pytest.mark.parametrize(
    ('username', 'password', 'status_code', 'msg'),
    (
            # create a new user 'admin'
            ('admin', '111', 409, 'user name cannot be admin'),

            # create a new user 'new_user'
            ('new_user', '1', 201, 'new_user'),

            # create a user which already exists
            ('test', '1', 409, "User 'test' already exists"),
    )
)
def test_post_method(jwt_auth, username, password, status_code, msg):
    """Test method 'POST'."""
    jwt_auth.login_as_admin()
    url = '/user'
    response = jwt_auth.post(url, {'name': username, 'password': password})
    assert response.status_code == status_code
    if msg:
        assert msg in str(json.loads(response.data))


@pytest.mark.parametrize(
    ('username', 'password', 'status_code', 'msg'),
    (
            # change password for user 'test'
            ('test', '111', 201, 'test'),

            # user not exists
            ('user_not_exists', '111', 403, None),
    )
)
def test_put_method(jwt_auth, username, password, status_code, msg):
    """Test method 'PUT'."""
    jwt_auth.login_as_admin()
    url = '/user'
    response = jwt_auth.post(url + '/' + username,
                             {'_method': 'put', 'password': password})
    assert response.status_code == status_code
    if msg:
        assert msg in str(response.data)


@pytest.mark.parametrize(
    ('username', 'password', 'status_code', 'msg'),
    (
            # change password for user 'test'
            ('test', '111', 201, 'test'),

            # user not exists
            ('user_not_exists', '111', 403, None),
    )
)
def test_put_method2(jwt_auth, username, password, status_code, msg):
    """Test method 'PUT2'."""
    jwt_auth.login_as_admin()
    url = '/user'
    response = jwt_auth.put(url + '/' + username, {'password': password})
    assert response.status_code == status_code
    if msg:
        assert msg in str(response.data)


def clear_table_user_info(jwt_auth):
    """Clear tale 'user_info'."""
    for username in ('test', 'test2'):
        assert jwt_auth.delete('userinfo/' + username).status_code == 200


@pytest.mark.parametrize(
    ('username', 'status_code'),
    (
            # user not exists
            ('user_not_exists', 404),

            # delete user 'test'
            ('test', 200),
    )
)
def test_delete_method(jwt_auth, username, status_code):
    """Test method 'DELETE'."""
    jwt_auth.login_as_admin()
    clear_table_user_info(jwt_auth)
    url = '/user'
    response = jwt_auth.post(url + '/' + username, {'_method': 'delete'})
    assert response.status_code == status_code


@pytest.mark.parametrize(
    ('username', 'status_code'),
    (
            # user not exists
            ('user_not_exists', 404),

            # delete user 'test'
            ('test', 200),
    )
)
def test_delete_method2(jwt_auth, username, status_code):
    """Test method 'DELETE2'."""
    jwt_auth.login_as_admin()
    clear_table_user_info(jwt_auth)
    url = '/user'
    response = jwt_auth.delete(url + '/' + username)
    assert response.status_code == status_code
