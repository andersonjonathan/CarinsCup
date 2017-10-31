#!/usr/bin/env python

from setuptools import setup

setup(
    name='CarinsCup',
    version='0.2',
    description='Carins Cup, the most prestigious orienteering cup',
    author='Jonathan Anderson',
    author_email='jonathan@jonathananderson.se',
    url='https://github.com/andersonjonathan/CarinsCup',
    install_requires=[
        'Django>=1.11.5',
        'mysqlclient',
        'dj-static==0.0.6',
        'Eventor-toolkit>=1.0.7',
        'pytz'
    ],
    dependency_links=[
        'https://github.com/andersonjonathan/Eventor-toolkit/tarball/master#egg=Eventor-toolkit-1.0.7',
    ],
)
