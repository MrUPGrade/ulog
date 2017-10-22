import logging

from ulog import ULog

logging.basicConfig(level=logging.DEBUG)
ulog = ULog()


class MyException(Exception):
    def __init__(self, context):
        self._context = context

    def __str__(self):
        return 'My exception with context: %s' % self._context


class TestClass(object):
    @ulog.log_return('Return from function {callable_name}: {return_value}')
    @ulog.log_exception(msg='OMG!', traceback=True)
    @ulog.log_args()
    def divide_func(self, x, y):
        return x / y


tc = TestClass()

try:
    tc.divide_func(0, 0)
except:
    pass

tc.divide_func(3, 2)
