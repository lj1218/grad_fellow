# -*- coding:utf-8 -*-
"""Test web console."""
import json


def login_as_admin(auth):
    """Login as admin."""
    response = auth.login_as_admin()
    resp_data = json.loads(response.data)
    assert response.status_code == 200
    assert resp_data['status'] == 0
    assert resp_data['next'] == '/'


def test_login_as_admin(client, auth):
    """Test login as admin."""
    response = auth.login('admin', '1')
    resp_data = json.loads(response.data)
    assert response.status_code == 401
    assert resp_data['status'] == 1
    assert resp_data['error'] == 'Incorrect password.'
    login_as_admin(auth)


def test_login_as_normal_user(client, auth):
    """Test login as normal user."""
    # test that only 'admin' is allow to login web console
    response = auth.login('test', '123456')
    resp_data = json.loads(response.data)
    assert response.status_code == 401
    assert resp_data['status'] == 1
    assert resp_data['error'] == 'Incorrect username.'


def get_page(client, auth, url):
    """Get page."""
    login_as_admin(auth)
    return client.get(url)


def test_administrator_management_page(client, auth):
    """Test administrator management page."""
    from grad_fellow.admin.webconsole.administrator import \
        block_title, url_prefix
    response = get_page(client, auth, url_prefix + '/')
    assert response.status_code == 200
    assert block_title in str(response.data)


def test_user_management_page(client, auth):
    """Test user management page."""
    from grad_fellow.admin.webconsole.user import block_title, url_prefix
    response = get_page(client, auth, url_prefix + '/')
    assert response.status_code == 200
    assert block_title in str(response.data)


def test_country_management_page(client, auth):
    """Test country management page."""
    from grad_fellow.admin.webconsole.country import block_title, url_prefix
    response = get_page(client, auth, url_prefix + '/')
    assert response.status_code == 200
    assert block_title in str(response.data)


def test_position_management_page(client, auth):
    """Test position management page."""
    from grad_fellow.admin.webconsole.position import block_title, url_prefix
    response = get_page(client, auth, url_prefix + '/')
    assert response.status_code == 200
    assert block_title in str(response.data)
