# -*- coding:utf-8 -*-
"""Access control list."""
import logging

from flask import request

logger = logging.getLogger(__name__)

rules_forbidden = {
    'admin': {
        'GET': [],
        'POST': ['/userinfo']
    },
    'others': {
        'GET': [
            '/user',
        ],
        'POST': [
            '/user',
            '/country',
            '/position',
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
            '/user/{!username}',  # deny 与当前用户不匹配的 request path
            '/userinfo/{!username}',
        ],
        'POST': [
            '/country/<int>',
            '/position/<int>',
            '/user/{!username}',  # deny 与当前用户不匹配的 request path
            '/userinfo/{!username}',
        ],
        'PUT': [
            '/userinfo/{!username}',
        ],
        'DELETE': [
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
    return check_access_permission0(
        user, request.path, request.url, request.method
    )


def check_access_permission0(user, path, url, method):
    """Check access permission.

    :param user: user name
    :param path: url path
    :param url: url
    :param method: http method
    :return: True - Allow
             False - Deny
    """
    logger.debug('request path: ' + path)
    logger.debug('request url: ' + url)
    logger.debug('request method: ' + method)
    logger.debug('### user: ' + user)

    if user != 'admin':
        user_in_rules = 'others'
    else:
        user_in_rules = user

    forbidden_paths = rules_forbidden.get(user_in_rules).get(method)
    if forbidden_paths and path in forbidden_paths:
        return False

    forbidden_paths_with_var = rules_forbidden_with_path_var.get(
        user_in_rules).get(method)
    # When http method not in rules, deny it.
    if forbidden_paths_with_var is None:
        return False

    for path_with_var in forbidden_paths_with_var:
        placeholder = '<int>'
        idx = path_with_var.find(placeholder)
        if idx != -1 and path_with_var[:idx] == path[:idx]:
            try:
                int(path[idx:])
                # matched
                return False
            except ValueError:
                pass

        placeholder = '{!username}'
        idx = path_with_var.find(placeholder)
        if idx != -1 and path_with_var[:idx] == path[:idx]:
            allow_path = path_with_var.replace(placeholder, user)
            return allow_path == path

    return True
