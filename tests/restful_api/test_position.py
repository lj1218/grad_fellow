# -*- coding:utf-8 -*-
"""Test position."""
import pytest


def test_unknown_method(client, jwt_auth):
    """Test unknown method xx."""
    jwt_auth.login_as_admin()
    response = jwt_auth.post('/position/1', {'_method': 'xx'})
    assert response.status_code == 403


@pytest.mark.parametrize(
    ('position_id', 'status_code', 'msgs'),
    (
            # get all positions
            (None, 200, [
                'Software EngineerSystem Analyst',
                'Business Analyst',
                'Technical support',
                'Network Engineer',
                'Technical Consultant',
                'Web Developer',
                'Software Test'
            ]),

            # position_id not exists
            ('0', 404, None),

            # position_id exists
            ('1', 200, ['Software EngineerSystem Analyst']),
    )
)
def test_get_method(client, position_id, status_code, msgs):
    """Test method 'GET'."""
    url = '/position' if position_id is None else '/position/' + position_id
    response = client.get(url)
    assert response.status_code == status_code
    if msgs:
        resp_data = str(response.get_json())
        for msg in msgs:
            assert msg in resp_data


@pytest.mark.parametrize(
    ('position', 'status_code', 'msg'),
    (
            # create a new position
            ('Database Administrator', 201, 'Database Administrator'),

            # create a position which already exists
            ('Business Analyst', 409, "'Business Analyst' already exists"),
    )
)
def test_post_method(jwt_auth, position, status_code, msg):
    """Test method 'POST'."""
    jwt_auth.login_as_admin()
    url = '/position'
    response = jwt_auth.post(url, {'name': position})
    assert response.status_code == status_code
    if msg:
        assert msg in str(response.get_json())


@pytest.mark.parametrize(
    ('position_id', 'new_position', 'status_code', 'msg'),
    (
            # change 'Business Analyst' => 'Web Developer'
            ('2', 'Web Developer', 409, None),

            # change 'Business Analyst' => 'Database Administrator'
            ('2', 'Database Administrator', 201, 'Database Administrator'),

            # position_id not exists
            ('0', 'Database Administrator', 403, None),
    )
)
def test_put_method(jwt_auth, position_id, new_position, status_code, msg):
    """Test method 'PUT'."""
    jwt_auth.login_as_admin()
    url = '/position'
    response = jwt_auth.post(url + '/' + position_id,
                             {'_method': 'put', 'name': new_position})
    assert response.status_code == status_code
    if msg:
        assert msg in str(response.data)


@pytest.mark.parametrize(
    ('position_id', 'new_position', 'status_code', 'msg'),
    (
            # change 'Business Analyst' => 'Web Developer'
            ('2', 'Web Developer', 409, None),

            # change 'Business Analyst' => 'Database Administrator'
            ('2', 'Database Administrator', 201, 'Database Administrator'),

            # position_id not exists
            ('0', 'Database Administrator', 403, None),
    )
)
def test_put_method2(jwt_auth, position_id, new_position, status_code, msg):
    """Test method 'PUT2'."""
    jwt_auth.login_as_admin()
    url = '/position'
    response = jwt_auth.put(url + '/' + position_id, {'name': new_position})
    assert response.status_code == status_code
    if msg:
        assert msg in str(response.data)


@pytest.mark.parametrize(
    ('position_id', 'status_code'),
    (
            # position_id not exists
            ('0', 404),

            # delete 'Software EngineerSystem Analyst'
            ('1', 200),
    )
)
def test_delete_method(jwt_auth, position_id, status_code):
    """Test method 'DELETE'."""
    jwt_auth.login_as_admin()
    url = '/position'
    response = jwt_auth.post(url + '/' + position_id, {'_method': 'delete'})
    assert response.status_code == status_code


@pytest.mark.parametrize(
    ('position_id', 'status_code'),
    (
            # position_id not exists
            ('0', 404),

            # delete 'Software EngineerSystem Analyst'
            ('1', 200),
    )
)
def test_delete_method2(jwt_auth, position_id, status_code):
    """Test method 'DELETE2'."""
    jwt_auth.login_as_admin()
    url = '/position'
    response = jwt_auth.delete(url + '/' + position_id)
    assert response.status_code == status_code
