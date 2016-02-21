import logging

from ulog import PythonLogger, ULog, LogLevel

backend = PythonLogger(python_logger=logging.getLogger())
backend.bootstrap_logger()
ulog = ULog(logger=backend, log_level=LogLevel.Debug)


class MyException(Exception):
    def __init__(self, context):
        self._context = context

    def __str__(self):
        return 'My exception with context: %s' % self._context


@ulog.log_return('Return from function {callable_name}: {return_value}')
@ulog.log_exception(msg='OMG!', traceback=True)
@ulog.log_args('X of {callable_name} is:', arguments=('x',))
def divide_func(x, y):
    return x / y


try:
    divide_func(0, 0)
except:
    pass

divide_func(3, 2)
