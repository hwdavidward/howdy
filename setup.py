# -*- coding: utf-8 -*-
"""
Howdy
------------
Search for a phone number from various social sources

"""
from setuptools import setup, find_packages


setup(
    name='Howdy',
    version='0.0.1',
    url='https://github.com/hwdavidward/howdy',
    author='David Ward',
    author_email='hwdavidward@gmail.com',
    description='Search for a phone number from various social sources',
    long_description=__doc__,
    py_modules=['howdy'],
    test_suite='tests.say_howdy',
    packages=find_packages(exclude=['tests']),
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'requests>=2.5.0'
    ]
)