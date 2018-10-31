# -*- coding:utf-8 -*-
"""Test acl."""
import pytest

from grad_fellow.common.acl import check_access_permission0


@pytest.mark.parametrize(('user', 'path', 'url', 'method', 'return_val'), (
    ('admin', '/userinfo', 'http://localhost', 'POST', False),
    ('admin', '/user', 'http://localhost', 'POST', True),
))
def test_check_access_permission_for_admin(
        user, path, url, method, return_val
):
    """Check access permission for admin."""
    assert return_val == check_access_permission0(user, path, url, method)


@pytest.mark.parametrize(('user', 'path', 'url', 'method', 'return_val'), (
    ('test', '/user', 'http://localhost', 'GET', False),
    ('test', '/user/test', 'http://localhost', 'GET', True),
    ('test', '/user/test2', 'http://localhost', 'GET', False),
    ('test', '/userinfo/test', 'http://localhost', 'GET', True),
    ('test', '/userinfo/test2', 'http://localhost', 'GET', False),

    ('test', '/user', 'http://localhost', 'POST', False),
    ('test', '/country', 'http://localhost', 'POST', False),
    ('test', '/position', 'http://localhost', 'POST', False),
    ('test', '/country/1', 'http://localhost', 'POST', False),
    ('test', '/country/a', 'http://localhost', 'POST', True),
    ('test', '/position/1', 'http://localhost', 'POST', False),
    ('test', '/user/test', 'http://localhost', 'POST', True),
    ('test', '/user/test2', 'http://localhost', 'POST', False),
    ('test', '/userinfo/test', 'http://localhost', 'POST', True),
    ('test', '/userinfo/test2', 'http://localhost', 'POST', False),

    ('test', '/userinfo/test', 'http://localhost', 'PUT', True),
    ('test', '/userinfo/test2', 'http://localhost', 'PUT', False),

    ('test', '/userinfo/test', 'http://localhost', 'DELETE', True),
    ('test', '/userinfo/test2', 'http://localhost', 'DELETE', False),

    ('test', '/userinfo/test', 'http://localhost', 'OPTION', False),
))
def test_check_access_permission_for_normal_users(
        user, path, url, method, return_val
):
    """Check access permission for normal users."""
    assert return_val == check_access_permission0(user, path, url, method)
