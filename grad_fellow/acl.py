# -*- coding:utf-8 -*-
from flask import request


rules_deny = {
    # 'admin': [
    #     {'path': '/add_user', 'method': 'GET'}
    # ]
}


def check_access_permission(user):
    print('request.path: ' + request.path)
    print('request.url: ' + request.url)
    print('request.method: ' + request.method)
    rule_deny = rules_deny.get(user)
    print(rule_deny)

    if not rule_deny:
        return True
    for rule in rule_deny:
        if rule['path'] == request.path and rule['method'] == request.method:
            return False
    return True
