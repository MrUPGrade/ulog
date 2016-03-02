# coding=utf-8
from __future__ import absolute_import

import wrapt
import inspect

from ulog._base import LogLevel


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
                      msg='Call: "{callable_name}" raised exception of type {exception_type}',
                      log_level=LogLevel.Error,
                      traceback=True):

        @wrapt.decorator
        def decorator(wrapped, instance, args, kwargs):
            if self._should_log(log_level):
                try:
                    result = wrapped(*args, **kwargs)
                except Exception as ex:
                    context = {'callable_name': wrapped.__name__,
                               'exception_type': type(ex),
                               'exception': ex}
                    log_message = msg.format(**context)
                    self._log(log_level, log_message, traceback)
                    raise

                return result

            else:
                return wrapped(*args, **kwargs)

        return decorator

    def log_args(self,
                 msg='Call: "{callable_name}" called with arguments',
                 arguments=None,
                 log_level=LogLevel.Debug):

        @wrapt.decorator
        def decorator(wrapped, instance, args, kwargs):
            if self._should_log(log_level):
                context = {
                    'callable_name': wrapped.__name__
                }
                log_message = msg.format(**context)

                if not arguments or len(arguments) == 0:
                    log_message += self._format_all_parameters(func=wrapped, args=args, kwargs=kwargs)
                else:
                    log_message += self._format_selected_params(arguments=arguments, func=wrapped, args=args,
                                                                kwargs=kwargs)
                self._log(log_level, log_message)

                result = wrapped(*args, **kwargs)

                return result

            else:
                return wrapped(*args, **kwargs)

        return decorator

    def log_return(self, msg='Call: "{callable_name}" returned value "{return_value}"', log_level=LogLevel.Debug):

        @wrapt.decorator
        def decorator(wrapped, instance, args, kwargs):
            if self._should_log(log_level):
                result = wrapped(*args, **kwargs)
                context = {
                    'callable_name': wrapped.__name__,
                    'return_value': result
                }
                log_message = msg.format(**context)
                self._log(log_level, log_message)

                return result

            else:
                return wrapped(*args, **kwargs)

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
