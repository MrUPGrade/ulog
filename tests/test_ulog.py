from __future__ import absolute_import

import pytest
import mock
from ulog import Logger
from ulog.logger import LoggerBackend, LogLevel


@pytest.fixture
def backend_mock():
    m = mock.create_autospec(LoggerBackend)
    return m


class FakeException(Exception):
    pass


def test_if_backend_is_called_corectly(backend_mock):
    logger = Logger(logging_backend=backend_mock)

    @logger.log_call_or_error(msg_before='before', msg_after='after', msg_error='error')
    def myfunc(a, b=10):
        return 0

    calls = [
        mock.call(LogLevel.Debug, 'before'),
        mock.call(LogLevel.Debug, 'after'),
    ]

    myfunc(1)

    backend_mock.log.assert_has_calls(calls)
    assert backend_mock.log.call_count == 2


def test_if_exception_is_logged(backend_mock):
    logger = Logger(logging_backend=backend_mock)

    @logger.log_call_or_error(msg_before='before', msg_after='after', msg_error='error')
    def myfunc(a, b=10):
        raise FakeException()

    calls = [
        mock.call(LogLevel.Debug, 'before'),
        mock.call(LogLevel.Debug, 'error'),
    ]

    with pytest.raises(FakeException):
        myfunc(1)

    backend_mock.log.assert_has_calls(calls)
    assert backend_mock.exception.call_count == 1
    assert backend_mock.log.call_count == 2


def test_if_logger_ignores_lower_levels(backend_mock):
    logger = Logger(logging_backend=backend_mock, log_level=LogLevel.Critical)

    @logger.log_call_or_error(msg_before='before', msg_after='after', msg_error='error', log_level=LogLevel.Debug)
    def myfunc():
        return 0

    assert backend_mock.exception.call_count == 0
    assert backend_mock.log.call_count == 0
