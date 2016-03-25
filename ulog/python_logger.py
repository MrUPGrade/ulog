# coding=utf-8
from __future__ import absolute_import

import logging
import logging.handlers

from ulog.base import LoggerBase, LogLevel


class PythonLogger(LoggerBase):
    LOG_LEVEL_MAP = {
        LogLevel.Critical: logging.CRITICAL,
        LogLevel.Error: logging.ERROR,
        LogLevel.Warning: logging.WARNING,
        LogLevel.Info: logging.INFO,
        LogLevel.Debug: logging.DEBUG,
        LogLevel.NotSet: logging.NOTSET
    }

    DEFAULT_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
    DEFAULT_TIME_FORMAT = "%Y-%m-%d %H:%M:%S"

    def __init__(self, python_logger):
        self._logger = python_logger

    def log(self, log_level, msg, traceback=False):
        logging_level = self._get_log_level(log_level)
        self._logger.log(logging_level, msg, exc_info=traceback)

    def bootstrap_logger(self):
        # type: () -> None
        self._logger_reset()

        stream_handler = logging.StreamHandler()
        formater = logging.Formatter(fmt=self.DEFAULT_FORMAT, datefmt=self.DEFAULT_TIME_FORMAT)
        stream_handler.setFormatter(formater)

        self._logger.addHandler(stream_handler)
        self._logger.setLevel(self._get_log_level(LogLevel.NotSet))

    def add_std_handler(self, handler):
        # type: () -> None
        self._logger.addHandler(handler)

    def _logger_reset(self):
        # type: () -> None
        map(self._logger.removeHandler, self._logger.handlers[:])
        map(self._logger.removeFilter, self._logger.filters[:])

    def _get_log_level(self, level):
        # type: (int) -> LogLevel
        return self.LOG_LEVEL_MAP[level]
