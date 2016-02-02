# coding=utf-8
from __future__ import absolute_import

import traceback
import logging

from ulog._base import LoggerBase, LogLevel


class PythonLogger(LoggerBase):
    LOG_LEVEL_MAP = {
        LogLevel.Critical: logging.CRITICAL,
        LogLevel.Error: logging.ERROR,
        LogLevel.Warning: logging.WARNING,
        LogLevel.Info: logging.INFO,
        LogLevel.Debug: logging.DEBUG,
        LogLevel.NotSet: logging.NOTSET
    }

    def __init__(self, python_logger):
        self._logger = python_logger

    def log(self, level, msg):
        logging_level = self._get_log_level(level)
        self._logger.log(logging_level, msg)

    def exception(self, level, msg, exception=None):
        stack_tracke = traceback.format_exc()
        message = '%s\n%s' % (msg, stack_tracke)
        self._logger.log(level.value, message)

    def _get_log_level(self, log_level):
        return self.LOG_LEVEL_MAP[log_level]
