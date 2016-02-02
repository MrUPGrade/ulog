# coding=utf-8
from __future__ import print_function, absolute_import

from ulog import ULog, LogLevel, PythonLogger

import logging
import logging.handlers


class MyException(Exception):
    def __init__(self, context):
        self._context = context

    def __str__(self):
        return 'My exception with context %s' % self._context


def test_one():
    # This is typical logger setup
    l = logging.getLogger('client')
    l.setLevel(logging.DEBUG)
    sw = logging.StreamHandler()
    sw.setFormatter(logging.Formatter(
        fmt="%(asctime)s - %(levelname)s - %(message)s",
        datefmt='%Y-%m-%d %H:%M:%S'))
    l.addHandler(sw)

    backend = PythonLogger(l)
    ulog = ULog(logger=backend, log_level=LogLevel.Debug)

    @ulog.log_exception(msg='This is a log message for error')
    def my_f():
        raise MyException('some context')


    @ulog.log_exception(msg='This is a log message for error')
    @ulog.log_return('return is: ')
    @ulog.log_params('log me:', ('x', 'y'))
    def my_f2(x, y):
        return x / y


    try:
         my_f2(2, 0)
    except Exception:
        pass
