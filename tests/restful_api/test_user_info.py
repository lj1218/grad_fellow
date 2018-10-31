# -*- coding:utf-8 -*-
"""Test user info."""
import pytest


@pytest.mark.parametrize(
    ('nationality', 'position', 'status_code'),
    (
            # get all user info where nationality='China' and \
            # position='Business Analyst'
            ('China', 'Business Analyst', 200),

            # get all user info where nationality='China'
            ('China', None, 200),

            # get all user info where position='Business Analyst'
            (None, 'Business Analyst', 200),

            # get all user info
            (None, None, 200),
    )
)
def test_user_infos_get_method(client, nationality, position, status_code):
    """Test method 'GET'."""
    url = '/userinfo'
    if nationality and position:
        url += '?nationality={0}&&position={1}'.format(nationality, position)
    elif nationality:
        url += '?nationality={0}'.format(nationality)
    elif position:
        url += '?position={0}'.format(position)
    response = client.get(url)
    assert response.status_code == status_code


@pytest.mark.parametrize(
    (
            'name', 'password', 'first_name', 'last_name', 'position',
            'company', 'nationality', 'tobe_contacted', 'skills_have',
            'skills_learned', 'status_code'
    ),
    (
            # update user info
            (
                    'test', '123456', 'Huang', 'Xiao', 'Business Analyst',
                    'Global Consulting Services', 'China', 1,
                    '3 months Python Subject',
                    'Advanced Python through on-job training', 201
            ),

            # create user info
            (
                    'test3', '123456', 'Huang', 'Xiao', 'Business Analyst',
                    'Global Consulting Services', 'China', 0,
                    '3 months Python Subject',
                    'Advanced Python through on-job training', 201
            ),

            # create user info
            (
                    'test3', '123456', 'Huang', 'Xiao', 'Business Analyst',
                    'Global Consulting Services', 'China', 'True',
                    '3 months Python Subject',
                    'Advanced Python through on-job training', 201
            ),

            # unauthorized user 'test4'
            (
                    'test4', '1', 'Huang', 'Xiao', 'Business Analyst',
                    'Global Consulting Services', 'China', 1,
                    '3 months Python Subject',
                    'Advanced Python through on-job training', 401
            ),
    )
)
def test_user_infos_post_method(
        jwt_auth, name, password, first_name, last_name, position, company,
        nationality, tobe_contacted, skills_have, skills_learned, status_code
):
    """Test method 'POST'."""
    jwt_auth.login(name, password)
    url = '/userinfo'
    response = jwt_auth.post(url, {
        'name': name, 'first_name': first_name, 'last_name': last_name,
        'position': position, 'company': company, 'nationality': nationality,
        'tobe_contacted': tobe_contacted, 'skills_have': skills_have,
        'skills_learned': skills_learned,
    })
    assert response.status_code == status_code


@pytest.mark.parametrize(
    ('name2login', 'password', 'name2query', 'status_code'),
    (
            # user info not exists
            ('user_not_exists', '1', 'user_not_exists', 401),

            # get user info for 'test' with wrong password
            ('test', '123', 'test', 401),

            # get user info for 'test'
            ('test', '123456', 'test', 200),

            # get user info for 'test2' login with user 'test' (forbidden)
            ('test', '123456', 'test2', 401),
    )
)
def test_user_info_get_method(jwt_auth, name2login, password,
                              name2query, status_code):
    """Test method 'GET'."""
    jwt_auth.login(name2login, password)
    url = '/userinfo/' + name2query
    response = jwt_auth.get(url)
    assert response.status_code == status_code


@pytest.mark.parametrize(
    (
            'name', 'password', 'first_name', 'last_name', 'position',
            'company', 'nationality', 'tobe_contacted', 'skills_have',
            'skills_learned', 'status_code'
    ),
    (
            # update user info
            (
                    'test', '123456', 'Huang', 'Xiao', 'Business Analyst',
                    'Global Consulting Services', 'China', 1,
                    '3 months Python Subject',
                    'Advanced Python through on-job training', 201
            ),

            # update user info which not exists
            (
                    'test3', '123456', 'Huang', 'Xiao', 'Business Analyst',
                    'Global Consulting Services', 'China', 0,
                    '3 months Python Subject',
                    'Advanced Python through on-job training', 403
            ),

            # unauthorized user 'test4'
            (
                    'test4', '1', 'Huang', 'Xiao', 'Business Analyst',
                    'Global Consulting Services', 'China', 1,
                    '3 months Python Subject',
                    'Advanced Python through on-job training', 401
            ),
    )
)
def test_user_info_put_method(
        jwt_auth, name, password, first_name, last_name, position, company,
        nationality, tobe_contacted, skills_have, skills_learned, status_code
):
    """Test method 'PUT'."""
    jwt_auth.login(name, password)
    url = '/userinfo/' + name
    response = jwt_auth.put(url, {
        'first_name': first_name, 'last_name': last_name,
        'position': position, 'company': company, 'nationality': nationality,
        'tobe_contacted': tobe_contacted, 'skills_have': skills_have,
        'skills_learned': skills_learned,
    })
    assert response.status_code == status_code


@pytest.mark.parametrize(
    ('name', 'password', 'status_code'),
    (
            # user info not exists
            ('user_not_exists', '1', 401),

            # delete user info for 'test' with wrong password
            ('test', '123', 401),

            # delete user info for 'test'
            ('test', '123456', 200),

            # delete user info for 'test3' which not exists
            ('test3', '123456', 404),
    )
)
def test_user_info_delete_method(jwt_auth, name, password, status_code):
    """Test method 'DELETE'."""
    jwt_auth.login(name, password)
    url = '/userinfo/' + name
    response = jwt_auth.delete(url)
    assert response.status_code == status_code
