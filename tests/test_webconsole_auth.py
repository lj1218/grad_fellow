# -*- coding:utf-8 -*-
"""Test web console auth."""
import pytest
from flask import g, session


def test_login_required(client):
    """Test login required."""
    response = client.get('/')
    assert response.status_code == 302
    assert response.headers['Location'] == 'http://localhost/auth/login'


def test_login(client, auth):
    """Test login."""
    # test that viewing the page renders without template errors
    assert client.get('/auth/login').status_code == 200

    # test that successful login redirects to the index page
    response = auth.login_as_admin()
    resp_data = response.get_json()
    assert resp_data['status'] == 0
    assert resp_data['next'] == '/'

    # login request set the name in the session
    # check that the user is loaded from the session
    with client:
        client.get('/')
        assert session['name'] == 'admin'
        assert g.user.name == 'admin'


@pytest.mark.parametrize(('username', 'password', 'message'), (
    ('123456', 'test', b'{"status": 1, "error": "Incorrect username."}'),
    ('test', '1', b'{"status": 1, "error": "Incorrect username."}'),
    ('test', '123456', b'{"status": 1, "error": "Incorrect username."}'),
    ('admin', '123456', b'{"status": 1, "error": "Incorrect password."}'),
    ('admin', '123', b'{"status": 0, "next": "/"}'),
))
def test_login_validate_input(auth, username, password, message):
    """Test login."""
    response = auth.login(username, password)
    assert message == response.data


def test_logout(client, auth):
    """Test logout."""
    response = auth.login_as_admin()
    assert response.data == b'{"status": 0, "next": "/"}'
    with client:
        response = auth.logout()
        assert 'name' not in session
        # test that successful logout redirects to the index page
        assert response.headers['Location'] == 'http://localhost/'
