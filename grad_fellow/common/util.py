# -*- coding:utf-8 -*-
"""Utilities."""
import os

from flask import request

try:
    from urllib.parse import urlparse, urljoin  # Python3
except ImportError:
    from urlparse import urlparse, urljoin  # Python2


def is_safe_url(target):
    """Check if target a safe url."""
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
        ref_url.netloc == test_url.netloc


def create_dir(path):
    """Create a directory."""
    if path == '':
        return
    if not os.path.exists(path):
        os.makedirs(path)


def write_file(file, content, encoding='utf-8'):
    """Write content to file."""
    create_dir(os.path.dirname(file))
    # print('Write file: {0}'.format(file))
    # with open(file, 'w', encoding=encoding) as f:  # Python3
    with open(file, 'w') as f:  # Python2
        f.write(content)


def save_pid(file='my.pid', encoding='utf-8'):
    """Save the current process id to file."""
    pid = os.getpid()
    write_file(file, str(pid), encoding=encoding)
