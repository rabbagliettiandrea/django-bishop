# -*- coding: utf-8 -*-

from __future__ import division

from setuptools import setup, find_packages
import subprocess
import shlex

GIT_HEAD_REV = subprocess.check_output(shlex.split('git rev-parse --short HEAD')).strip()


setup(
    name='django-bishop',
    version='0.1.dev#%s' % GIT_HEAD_REV,
    packages=find_packages(),
    include_package_data=True,
    url='https://github.com/silverfix/django-bishop',
    license='BSD',
    author='Andrea Rabbaglietti',
    author_email='rabbagliettiandrea@gmail.com',
    description='A bunch of useful devops script to support django projects',
    install_requires=[
        'django>=1.8'
    ]
)
