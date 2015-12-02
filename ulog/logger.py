from __future__ import absolute_import
import logging
import abc
import six
import enum
from functools import wraps

logging.basicConfig(level=logging.INFO)


class LogLevel(enum.IntEnum):
    Critical = 0
    Error = 1
    Warning = 2
    Info = 3
    Debug = 4
    No = 99


@six.add_metaclass(abc.ABCMeta)
class LoggerBackend(object):
    @abc.abstractmethod
    def log(self, level, msg):
        pass

    @abc.abstractmethod
    def exception(self, exception):
        pass


class PythonLoggerBackend(LoggerBackend):
    LOG_LEVEL_MAP = {
        LogLevel.Critical: logging.CRITICAL,
        LogLevel.Error: logging.ERROR,
        LogLevel.Warning: logging.WARNING,
        LogLevel.Info: logging.INFO,
        LogLevel.Debug: logging.DEBUG
    }

    def __init__(self):
        self._logger = logging.getLogger()

    def log(self, level, msg):
        logging_level = self._get_log_level(level)
        self._logger.log(logging_level, msg)

    def exception(self, exception):
        self._logger.exception(exception)

    def _get_log_level(self, log_level):
        return self.LOG_LEVEL_MAP[log_level]


class Logger(object):
    def __init__(self, logging_backend=None, log_level=LogLevel.Error):
        self._logger = logging_backend or PythonLoggerBackend()
        self._log_level = log_level

    def log_call_or_error(self, msg_before=None, msg_after=None, msg_error=None, log_level=LogLevel.Debug):
        def decorator(func):
            @wraps(func)
            def inner(*args, **kwargs):

                if msg_before:
                    self._log(log_level, msg_before)
                try:
                    result = func(*args, **kwargs)
                except Exception as ex:
                    if msg_error:
                        self._log(log_level, msg_error)
                    self._logger.exception(ex)
                    raise

                if msg_after:
                    self._log(log_level, msg_after)

                return result

            return inner

        return decorator

    def _log(self, level, msg):
        if level >= self._log_level:
            self._logger.log(level, msg)
