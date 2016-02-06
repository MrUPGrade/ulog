# coding=utf-8
from __future__ import print_function, absolute_import

from ulog import ULog, LogLevel, PythonLogger

import pytest
import logging
import logging.handlers


class MyException(Exception):
    def __init__(self, context):
        self._context = context

    def __str__(self):
        return 'My exception with context %s' % self._context


@pytest.fixture(scope='session')
def pylogger():
    # This is typical logger setup
    logger = logging.getLogger('client')
    logger.setLevel(logging.DEBUG)
    sw = logging.StreamHandler()
    sw.setFormatter(logging.Formatter(
        fmt="%(asctime)s - %(levelname)s - %(message)s",
        datefmt='%Y-%m-%d %H:%M:%S'))
    logger.addHandler(sw)
    return logger


def test_one(pylogger):
    backend = PythonLogger(python_logger=pylogger)
    ulog = ULog(logger=backend, log_level=LogLevel.Debug)

    @ulog.log_exception(msg='This is a log message for error')
    def my_f():
        raise MyException('some context')

    @ulog.log_exception(msg='This is a log message for error')
    @ulog.log_return('return is: ')
    @ulog.log_selected_params('log me:', ('x', 'y'))
    def my_f2(x, y):
        return x / y

    my_f2(2, 1)

    try:
        my_f()
    except Exception:
        pass


def test_two(pylogger):
    backend = PythonLogger(python_logger=pylogger)
    ulog = ULog(logger=backend, log_level=LogLevel.Debug)

    @ulog.log_params(msg='This is my message')
    def my_f3(x, y, kw1=''):
        pass

    my_f3(1, 2)
