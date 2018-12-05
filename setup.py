#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""Setup script."""
import io
import re
from os import path

from setuptools import find_packages, setup

# with io.open('README.md', 'rt', encoding='utf8') as f:
#     readme = f.read()

version_file = path.join(path.dirname(__file__), 'grad_fellow', '__init__.py')
with io.open(version_file, 'rt', encoding='utf8') as f:
    version = re.search(r'__version__ = \'(.*?)\'', f.read()).group(1)

setup(
    name='Grad-Fellow',
    version=version,
    url='',
    license='BSD',
    author='lj1218',
    author_email='lj_ebox@163.com',
    maintainer='lj1218',
    maintainer_email='lj_ebox@163.com',
    description='Grad fellow website.',
    # long_description=readme,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
        'flask_cors',
        'flask_restful',
        'flask_sqlalchemy',
        'flask_jwt',
        'mysqlclient',
        'waitress',
    ],
    extras_require={
        'test': [
            'pytest',
            'coverage',
        ],
    },
)
