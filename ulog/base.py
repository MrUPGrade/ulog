# coding=utf-8
from __future__ import absolute_import

import abc

import enum
import six


@enum.unique
class LogLevel(enum.IntEnum):
    Critical = 50
    Error = 40
    Warning = 30
    Info = 20
    Debug = 10
    NotSet = 0


@six.add_metaclass(abc.ABCMeta)
class LoggerBase(object):
    @abc.abstractmethod
    def log(self, level, msg, traceback=False):
        pass
