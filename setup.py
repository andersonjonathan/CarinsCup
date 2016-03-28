#!/usr/bin/env python

from setuptools import setup

setup(
    name='CarinsCup',
    version='0.1',
    description='Carins Cup, the most prestigious orienteering cup',
    author='Jonathan Anderson',
    author_email='jonathan@jonathananderson.se',
    url='https://github.com/andersonjonathan/CarinsCup',
    install_requires=[
        'Django==1.8.5'
    ],
    dependency_links=[
        'https://pypi.python.org/simple/django/'
    ],
)
