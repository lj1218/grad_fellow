# -*- coding:utf-8 -*-
"""Access control list."""
from flask import request

rules_forbidden = {
    'admin': {
        'GET': [],
        'POST': ['/userinfo']
    },
    'others': {
        'GET': [
            '/user', '/add_user',
            '/add_country', '/add_position'
        ],
        'POST': [
            '/user',
            '/country',
            '/add_country',
            '/position',
            '/add_position',
        ]
    }
}

rules_forbidden_with_path_var = {
    'admin': {
        'GET': [],
        'POST': [],
        'PUT': [],
        'DELETE': [],
    },
    'others': {
        'GET': [
            '/update_user/{!username}', '/delete_user/{!username}',
            '/update_country/<int>',     '/delete_country/<int>',
            '/update_position/<int>', '/delete_position/<int>',
            '/user/{!username}',  # deny 与当前用户不匹配的 request path
            '/userinfo/{!username}',
        ],
        'POST': [
            '/country/<int>',
            '/position/<int>',
            '/user/{!username}',  # deny 与当前用户不匹配的 request path
            '/userinfo/{!username}',
        ]
    }
}


def check_access_permission(user):
    """Check access permission.

    :param user: user name
    :return: True - Allow
             False - Deny
    """
    print('request.path: ' + request.path)
    print('request.url: ' + request.url)
    print('request.method: ' + request.method)
    print('### user: ' + user)

    if user != 'admin':
        user_in_rules = 'others'
    else:
        user_in_rules = user

    forbidden_paths = rules_forbidden.get(user_in_rules).get(request.method)
    if forbidden_paths and request.path in forbidden_paths:
        return False

    forbidden_paths_with_var = rules_forbidden_with_path_var.get(
        user_in_rules).get(request.method)
    # When http method not in rules, deny it.
    if forbidden_paths_with_var is None:
        return False

    for path_with_var in forbidden_paths_with_var:
        placeholder = '<int>'
        idx = path_with_var.find(placeholder)
        if idx != -1 and path_with_var[:idx] == request.path[:idx]:
            try:
                int(request.path[idx:])
                # matched
                return False
            except ValueError:
                pass

        placeholder = '{!username}'
        idx = path_with_var.find(placeholder)
        if idx != -1 and path_with_var[:idx] == request.path[:idx]:
            allow_path = path_with_var.replace(placeholder, user)
            return allow_path == request.path

    return True
