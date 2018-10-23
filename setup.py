# -*- coding:utf-8 -*-
"""Setup script."""
# import io

from setuptools import find_packages, setup

# with io.open('README.md', 'rt', encoding='utf8') as f:
#     readme = f.read()

setup(
    name='grad_fellow',
    version='1.0.0',
    url='',
    license='BSD',
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
        'flask_wtf',
        'sqlalchemy',
        'werkzeug',
        'wtforms',
        'mysqlclient',
    ],
    extras_require={
        'test': [
            'pytest',
            'coverage',
        ],
    },
)
