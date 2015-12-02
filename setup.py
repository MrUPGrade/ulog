# coding=utf-8
import sys
from setuptools import setup
from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


setup(
    name='ulog',
    version='0.0.1',
    packages=['ulog'],
    url='https://github.com/MrUPGrade/ulog',
    license='MIT',
    author='Jakub (Mr. UPGrade) Czapliński',
    author_email='sirupgrade@gmail.com',
    description='Simple decorator based logger',
    install_requires=[
        'six',
        'enum34'
    ],
    test_suite='tests',
    tests_require=[
        'pytest==2.7.3',
        'mock==1.0.1',
        'coverage==4.0.0'
    ],
    cmdclass={'test': PyTest},
    classifiers=[
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4"
        "Programming Language :: Python :: 3.5"
    ]
)
