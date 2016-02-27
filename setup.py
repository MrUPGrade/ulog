# coding=utf-8
from __future__ import absolute_import

from setuptools import setup

setup(
    name='ulog',
    version='0.1.0',
    packages=['ulog'],
    url='https://github.com/MrUPGrade/ulog',
    license='MIT',
    author='Jakub (Mr. UPGrade) Czapliński',
    author_email='sirupgrade@gmail.com',
    description='Simple decorator based logger',
    install_requires=[
        'six',
        'enum34',
        'funcsigs>=0.4',
        'future',
	'wrapt>=1.10.6'
    ],
    test_suite='tests',
    extras_require={
        'test': ['coverage>=4.0.0',
                 'mock>=1.3',
                 'pytest'],
        'dev': ['ipython']
    },
    classifiers=[
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5"
    ]
)
