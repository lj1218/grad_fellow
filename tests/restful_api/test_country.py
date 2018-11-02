# -*- coding:utf-8 -*-
"""Test country."""
import pytest


def test_unknown_method(client, jwt_auth):
    """Test unknown method xx."""
    jwt_auth.login_as_admin()
    response = jwt_auth.post('/country/1', {'_method': 'xx'})
    assert response.status_code == 403


@pytest.mark.parametrize(
    ('country_id', 'status_code', 'msgs'),
    (
            # get all countries
            (None, 200, ['China', 'India']),

            # country_id not exists
            ('0', 404, None),

            # country_id exists
            ('1', 200, ['China']),
    )
)
def test_get_method(client, country_id, status_code, msgs):
    """Test method 'GET'."""
    url = '/country' if country_id is None else '/country/' + country_id
    response = client.get(url)
    assert response.status_code == status_code
    if msgs:
        resp_data = str(response.get_json())
        for msg in msgs:
            assert msg in resp_data


@pytest.mark.parametrize(
    ('country', 'status_code', 'msg'),
    (
            # create a new country
            ('America', 201, 'America'),

            # create a country which already exists
            ('China', 409, "'China' already exists"),
    )
)
def test_post_method(jwt_auth, country, status_code, msg):
    """Test method 'POST'."""
    jwt_auth.login_as_admin()
    url = '/country'
    response = jwt_auth.post(url, {'name': country})
    assert response.status_code == status_code
    if msg:
        assert msg in str(response.get_json())


@pytest.mark.parametrize(
    ('country_id', 'new_country', 'status_code', 'msg'),
    (
            # change 'India' => 'China'
            ('2', 'China', 409, None),

            # change 'India' => 'Japan'
            ('2', 'Japan', 201, 'Japan'),

            # country_id not exists
            ('0', 'Japan', 403, None),
    )
)
def test_put_method(jwt_auth, country_id, new_country, status_code, msg):
    """Test method 'PUT'."""
    jwt_auth.login_as_admin()
    url = '/country'
    response = jwt_auth.post(url + '/' + country_id,
                             {'_method': 'put', 'name': new_country})
    assert response.status_code == status_code
    if msg:
        assert msg in str(response.data)


@pytest.mark.parametrize(
    ('country_id', 'new_country', 'status_code', 'msg'),
    (
            # change 'India' => 'China'
            ('2', 'China', 409, None),

            # change 'India' => 'Japan'
            ('2', 'Japan', 201, 'Japan'),

            # country_id not exists
            ('0', 'Japan', 403, None),
    )
)
def test_put_method2(jwt_auth, country_id, new_country, status_code, msg):
    """Test method 'PUT2'."""
    jwt_auth.login_as_admin()
    url = '/country'
    response = jwt_auth.put(url + '/' + country_id, {'name': new_country})
    assert response.status_code == status_code
    if msg:
        assert msg in str(response.data)


@pytest.mark.parametrize(
    ('country_id', 'status_code'),
    (
            # country_id not exists
            ('0', 404),

            # delete 'China'
            ('1', 200),
    )
)
def test_delete_method(jwt_auth, country_id, status_code):
    """Test method 'DELETE'."""
    jwt_auth.login_as_admin()
    url = '/country'
    response = jwt_auth.post(url + '/' + country_id, {'_method': 'delete'})
    assert response.status_code == status_code


@pytest.mark.parametrize(
    ('country_id', 'status_code'),
    (
            # country_id not exists
            ('0', 404),

            # delete 'China'
            ('1', 200),
    )
)
def test_delete_method2(jwt_auth, country_id, status_code):
    """Test method 'DELETE2'."""
    jwt_auth.login_as_admin()
    url = '/country'
    response = jwt_auth.delete(url + '/' + country_id)
    assert response.status_code == status_code
