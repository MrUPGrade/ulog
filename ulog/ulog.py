# coding=utf-8
from __future__ import absolute_import

from functools import wraps

from ulog._base import LogLevel

import inspect


class UnknownArgumentException(Exception):
    def __init__(self, argument):
        self._argument = argument

    def __str__(self):
        return 'Unknown argument %s' % self._argument

    def __unicode__(self):
        return self.__str__()


class NoArgumentProvided(Exception):
    def __init__(self, argument, argument_position):
        self._argument = argument
        self._argument_position = argument_position

    def __str__(self):
        return "Caller didn't provide a required positional parameter '%s' at index %d" % (
            self._argument, self._argument_position)


def get_argument(argument, func, args, kwargs):
    if argument in kwargs:
        return kwargs[argument]
    else:
        argspec = inspect.getargspec(func)
        if argument in argspec.args:
            argument_index = argspec.args.index(argument)
            if len(args) > argument_index:
                return args[argument_index]
            if argspec.defaults is not None:
                defaults_index = argument_index - len(argspec.args) + len(argspec.defaults)
                if 0 <= defaults_index < len(argspec.defaults):
                    return argspec.defaults[defaults_index]
            raise NoArgumentProvided(argument=argument, argument_position=argument_index)
        else:
            raise UnknownArgumentException(argument=argument)


class ULog(object):
    DEFAULT_PARAMETER_FORMAT = "\n%s: %s"

    def __init__(self, logger, log_level=LogLevel.Error):
        self._logger = logger
        self._log_level = log_level
        self._parameter_format = self.DEFAULT_PARAMETER_FORMAT

    def log_exception(self,
                      msg='Call: "{callable_name}" raised exception:',
                      log_level=LogLevel.Error,
                      traceback=True):
        def decorator(func):
            @wraps(func)
            def inner(*args, **kwargs):
                if self._should_log(log_level):
                    try:
                        result = func(*args, **kwargs)
                    except Exception as ex:
                        log_message = msg.format(**{'callable_name': func.__name__, 'exception': ex})
                        self._log(log_level, log_message, traceback)
                        raise

                    return result

                else:
                    return func(*args, **kwargs)

            return inner

        return decorator

    def log_args(self,
                 msg='Call: "{callable_name}" with arguments:',
                 arguments=None,
                 log_level=LogLevel.Debug):
        def decorator(func):
            @wraps(func)
            def inner(*args, **kwargs):
                if self._should_log(log_level):
                    log_message = msg.format(**{'callable_name': func.__name__})
                    if not arguments or len(arguments) == 0:
                        log_message += self._format_all_parameters(func=func, args=args, kwargs=kwargs)
                    else:
                        log_message += self._format_selected_params(arguments=arguments, func=func, args=args,
                                                                    kwargs=kwargs)
                    self._log(log_level, log_message)

                    result = func(*args, **kwargs)

                    return result

                else:
                    return func(*args, **kwargs)

            return inner

        return decorator

    def log_return(self, msg='Call: "{callable_name}" returned value: "{return_value}"', log_level=LogLevel.Debug):
        def decorator(func):
            @wraps(func)
            def inner(*args, **kwargs):
                if self._should_log(log_level):
                    result = func(*args, **kwargs)

                    log_message = msg.format(**{'callable_name': func.__name__, 'return_value': result})
                    self._log(log_level, log_message)

                    return result

                else:

                    return func(*args, **kwargs)

            return inner

        return decorator

    def _log(self, level, msg, traceback=False):
        self._logger.log(level, msg, traceback)

    def _format_selected_params(self, arguments, func, args, kwargs):
        log_message = ''

        for selecte_arg in arguments:
            param_value = get_argument(selecte_arg, func, args, kwargs)
            log_message += self._parameter_format % (selecte_arg, param_value)
        return log_message

    def _format_all_parameters(self, func, args, kwargs):
        log_message = ''
        func_args = inspect.getargspec(func)

        for i in range(0, len(args)):
            log_message += self._parameter_format % (func_args.args[i], args[i])

        for name, value in kwargs.items():
            log_message += self._parameter_format % (name, value)

        return log_message

    def _should_log(self, level):
        return level >= self._log_level
