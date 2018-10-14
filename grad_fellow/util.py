# -*- coding:utf-8 -*-
import os
try:
    # Python3
    from urllib.parse import urlparse, urljoin
except:
    # Python2
    from urlparse import urlparse, urljoin
from flask import request


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc


def create_dir(path):
    if path == '':
        return
    if not os.path.exists(path):
        os.makedirs(path)


def write_file(file, content, encoding='utf-8'):
    create_dir(os.path.dirname(file))
    print('Write file: {0}'.format(file))
    # with open(file, 'w', encoding=encoding) as f:  # Python3
    with open(file, 'w') as f:  # Python2
        f.write(content)


def save_pid(file='my.pid', encoding='utf-8'):
    pid = os.getpid()
    write_file(file, str(pid), encoding=encoding)
