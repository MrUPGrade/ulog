# coding=utf-8
from __future__ import absolute_import

from functools import wraps

from ulog._base import LogLevel

import inspect


def extract_param_by_name(f, args, kwargs, param):
    if param in kwargs:
        return kwargs[param]
    else:
        argspec = inspect.getargspec(f)
        if param in argspec.args:
            param_index = argspec.args.index(param)
            if len(args) > param_index:
                return args[param_index]
            if argspec.defaults is not None:
                # argsec.defaults holds the values for the LAST entries of argspec.args
                defaults_index = param_index - len(argspec.args) + len(argspec.defaults)
                if 0 <= defaults_index < len(argspec.defaults):
                    return argspec.defaults[defaults_index]
            raise LoggerBadCallerParametersException(
                "Caller didn't provide a required positional parameter '%s' at index %d", param, param_index)
        else:
            raise LoggerUnknownParamException("Unknown param %s(%r) on %s", type(param), param, f.__name__)


class LoggerUnknownParamException(Exception):
    pass


class LoggerBadCallerParametersException(Exception):
    pass


class ULog(object):
    def __init__(self, logger, log_level=LogLevel.Error):
        self._logger = logger
        self._log_level = log_level

    def log_exception(self, msg, log_level=LogLevel.Debug):
        def decorator(func):
            @wraps(func)
            def inner(*args, **kwargs):
                try:
                    result = func(*args, **kwargs)
                except Exception as ex:
                    self._log_exception(log_level, msg, ex)

                    raise

                return result

            return inner

        return decorator

    def log_selected_params(self, msg, params, log_level=LogLevel.Debug):
        def decorator(func):
            @wraps(func)
            def inner(*args, **kwargs):
                log_message = msg
                for param in params:
                    param_value = extract_param_by_name(func, args, kwargs, param)
                    log_message += "\n\t%s: %s" % (param, param_value)

                self._log(log_level, log_message)

                result = func(*args, **kwargs)

                return result

            return inner

        return decorator

    def log_params(self, msg='Function call: {func_name}', log_level=LogLevel.Debug):
        def decorator(func):
            @wraps(func)
            def inner(*args, **kwargs):
                log_message = msg.format({'func_name': func.__name__})
                func_args = inspect.getargspec(func)

                for i in range(0, len(args)):
                    log_message += "\n\t%s: %s" % (func_args.args[i], args[i])

                for name, value in kwargs.items():
                    log_message += "\n\t%s: %s" % (name, value)

                self._log(log_level, log_message)

                result = func(*args, **kwargs)

                return result

            return inner

        return decorator

    def log_return(self, msg, log_level=LogLevel.Debug):
        def decorator(func):
            @wraps(func)
            def inner(*args, **kwargs):
                result = func(*args, **kwargs)

                log_result = msg + str(result)
                self._log(log_level, log_result)

                return result

            return inner

        return decorator

    def _log(self, level, msg):
        if level >= self._log_level:
            self._logger.log(level, msg)

    def _log_exception(self, level, msg, exception=None):
        if level >= self._log_level:
            self._logger.exception(level, msg, exception)
