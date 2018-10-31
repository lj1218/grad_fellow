# -*- coding:utf-8 -*-
"""Test administrator."""


def test_administrator(client, jwt_auth):
    """Test administrator."""
    username = 'admin'
    password = '123'
    new_password = '123456'
    assert jwt_auth.login(username, password).status_code == 200
    # change admin's password
    response = jwt_auth.put('/administrator/admin',
                            {'name': username, 'password': new_password})
    assert response.status_code == 201

    # use old password to login, it should fail
    assert jwt_auth.login(username, password).status_code == 401

    # use new password to login, it should success
    assert jwt_auth.login(username, new_password).status_code == 200

    # delete admin from db
    response = jwt_auth.delete('/administrator/admin')
    assert response.status_code == 200
    assert b'delete admin success' in response.data

    # change password again, it should fail
    response = jwt_auth.put('/administrator/admin',
                            {'name': username, 'password': new_password})
    assert response.status_code == 401

    # use new password to login, it should fail
    assert jwt_auth.login(username, new_password).status_code == 401
