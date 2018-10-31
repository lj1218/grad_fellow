# -*- coding:utf-8 -*-
"""Test auth."""
import pytest


def test_login(client, jwt_auth):
    """Test jwt login."""
    response = jwt_auth.login_as_admin()
    assert response.status_code == 200
    assert 'access_token' in str(response.data)


@pytest.mark.parametrize(
    ('username', 'password', 'message', 'status_code'),
    (
            ('123456', 'test', b'Invalid credentials', 401),
            ('test', '123456', b'access_token', 200),
            ('123', 'admin', b'Invalid credentials', 401),
            ('admin', '123', b'access_token', 200),
    )
)
def test_login_validate_input(jwt_auth, username, password,
                              message, status_code):
    """Test login."""
    response = jwt_auth.login(username, password)
    assert response.status_code == status_code
    assert message in response.data
