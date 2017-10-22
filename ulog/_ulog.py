# coding=utf-8
from __future__ import absolute_import

import inspect
import logging

import enum
import wrapt


@enum.unique
class LogLevel(enum.IntEnum):
    Critical = 50
    Error = 40
    Warning = 30
    Info = 20
    Debug = 10
    NotSet = 0


LOG_LEVEL_MAP = {
    LogLevel.Critical: logging.CRITICAL,
    LogLevel.Error: logging.ERROR,
    LogLevel.Warning: logging.WARNING,
    LogLevel.Info: logging.INFO,
    LogLevel.Debug: logging.DEBUG,
    LogLevel.NotSet: logging.NOTSET
}


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


def get_argument(argument, func, args, kwargs, skip_instance=False):
    if argument in kwargs:
        return kwargs[argument]
    else:
        argspec = inspect.getargspec(func)
        if argument in argspec.args:
            argument_index = argspec.args.index(argument)
            if skip_instance:
                argument_index -= 1
            if len(args) > argument_index:
                return args[argument_index]
            if argspec.defaults is not None:
                defaults_index = argument_index - len(argspec.args) + len(argspec.defaults)
                if 0 <= defaults_index < len(argspec.defaults):
                    return argspec.defaults[defaults_index]
            raise NoArgumentProvided(argument=argument, argument_position=argument_index)
        else:
            raise UnknownArgumentException(argument=argument)


def prepare_common_context(wrapped, instance):
    context = {
        'func_name': wrapped.__name__,
    }
    if instance:
        context['class_name'] = instance.__class__.__name__
        context['callable_name'] = '{class_name}.{func_name}'.format(**context)
    else:
        context['callable_name'] = context['func_name']

    return context

class ULog(object):
    DEFAULT_PARAMETER_FORMAT = "\n%s: %s"

    def __init__(self, name='root', logger=None):
        self._python_logger = logger
        self._logger_name = name
        self._parameter_format = self.DEFAULT_PARAMETER_FORMAT

    def log_exception(self,
                      msg='Call: "{callable_name}" raised exception of type {exception_type}',
                      level=LogLevel.Error,
                      traceback=True):
        # type: (str, Union[LogLevel,int], bool) -> FunctionWrapper

        @wrapt.decorator
        def decorator(wrapped, instance, args, kwargs):
            try:
                result = wrapped(*args, **kwargs)
            except Exception as ex:
                context = {'callable_name': wrapped.__name__,
                           'exception_type': type(ex),
                           'exception': ex}
                log_message = msg.format(**context)
                self._log(level, log_message, traceback)
                raise

            return result

        return decorator

    def log_args(self,
                 msg='Call: "{callable_name}" called with arguments',
                 arguments=None,
                 level=LogLevel.Debug):
        # type: (str, Union[Tuple[str], None], LogLevel) -> FunctionWrapper

        @wrapt.decorator
        def decorator(wrapped, instance, args, kwargs):
            context = {
                'callable_name': wrapped.__name__
            }
            log_message = msg.format(**context)

            skip_instance = instance is not None

            if not arguments or len(arguments) == 0:
                log_message += self._format_all_parameters(func=wrapped,
                                                           args=args,
                                                           kwargs=kwargs,
                                                           skip_instance=skip_instance)
            else:
                log_message += self._format_selected_params(arguments=arguments,
                                                            func=wrapped,
                                                            args=args,
                                                            kwargs=kwargs,
                                                            skip_instance=skip_instance)
            self._log(level, log_message)

            result = wrapped(*args, **kwargs)

            return result

        return decorator

    def log_return(self, msg='Call: "{callable_name}" returned value "{return_value}"', level=LogLevel.Debug):
        # type: (str, Union[LogLevel, int]) -> FunctionWrapper
        @wrapt.decorator
        def decorator(wrapped, instance, args, kwargs):
            result = wrapped(*args, **kwargs)
            context = {
                'callable_name': wrapped.__name__,
                'return_value': result
            }
            log_message = msg.format(**context)
            self._log(level, log_message)

            return result

        return decorator

    def log_call(self, msg='Call: "{callable_name}"', level=LogLevel.Debug):
        @wrapt.decorator
        def decorator(wrapped, instance, args, kwargs):
            context = prepare_common_context(wrapped, instance)
            log_message = msg.format(**context)
            self._log(level, log_message)

            result = wrapped(*args, **kwargs)
            return result

        return decorator

    @property
    def logger(self):
        if not self._python_logger:
            self._python_logger = logging.getLogger(self._logger_name)

        return self._python_logger

    def _log(self, level, msg, traceback=False):
        if type(level) == LogLevel:
            python_level = LOG_LEVEL_MAP[level]
        else:
            python_level = level

        self.logger.log(python_level, msg, exc_info=traceback)

    def _format_selected_params(self, arguments, func, args, kwargs, skip_instance):
        log_message = ''

        for selecte_arg in arguments:
            param_value = get_argument(selecte_arg, func, args, kwargs, skip_instance)
            log_message += self._parameter_format % (selecte_arg, param_value)
        return log_message

    def _format_all_parameters(self, func, args, kwargs, skip_instance):
        log_message = ''
        func_args_info = inspect.getargspec(func)

        func_args = func_args_info.args

        if skip_instance:
            func_args = func_args[1:]

        for i in range(0, len(args)):
            log_message += self._parameter_format % (func_args[i], args[i])

        for name, value in kwargs.items():
            log_message += self._parameter_format % (name, value)

        return log_message
