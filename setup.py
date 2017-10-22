# coding=utf-8
from __future__ import absolute_import

from setuptools import setup

setup(
    name='ulog',
    version='0.3.2',
    packages=['ulog'],
    url='https://github.com/MrUPGrade/ulog',
    license='MIT',
    author='Jakub (Mr. UPGrade) Czapliński',
    author_email='sirupgrade@gmail.com',
    description='Simple decorator based logger',
    install_requires=[
        'six>=1.10.0',
        'enum34',
        'funcsigs>=0.4',
        'future',
        'wrapt>=1.10.6'
    ],
    test_suite='tests',
    extras_require={
        'test': [
            'coverage>=4.0.0',
            'mock>=1.3',
            'pytest',
            'pytest-cov',
        ],
        'dev': [
            'ipython',
            'wheel',
        ]
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
    ]
)
