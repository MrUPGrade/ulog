# coding=utf-8
from __future__ import absolute_import

import pytest
import mock

from ulog import ULog, LogLevel, LoggerBase

ERROR_MSG = 'msg'


@pytest.fixture
def backend_mock():
    m = mock.create_autospec(LoggerBase)
    return m


class FakeException(Exception):
    pass


class Test_ULog(object):
    def test_if_logger_is_called_for_loggin_exception(self, backend_mock):
        logger = ULog(logger=backend_mock, log_level=LogLevel.Debug)

        exception = FakeException()

        @logger.log_exception(msg=ERROR_MSG)
        def myfunc():
            raise exception

        with pytest.raises(FakeException):
            myfunc()

        backend_mock.exception.assert_called_once_with(LogLevel.Debug, ERROR_MSG,exception)

    def test_if_lower_levels_are_ignored(self, backend_mock):
        logger = ULog(logger=backend_mock, log_level=LogLevel.Critical)

        exception = FakeException()

        @logger.log_exception(ERROR_MSG, log_level=LogLevel.Debug)
        def myfunc():
            raise exception

        with pytest.raises(FakeException):
            myfunc()

        assert backend_mock.exception.call_count == 0

    def test_if_the_same_log_level_is_loged(self, backend_mock):
        logger = ULog(logger=backend_mock, log_level=LogLevel.Debug)

        exception = FakeException()

        @logger.log_exception(ERROR_MSG, log_level=LogLevel.Debug)
        def myfunc():
            raise exception

        with pytest.raises(FakeException):
            myfunc()

        assert backend_mock.exception.call_count == 1
