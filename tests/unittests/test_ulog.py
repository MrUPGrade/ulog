# coding=utf-8
from __future__ import absolute_import

import pytest
import mock

from ulog import ULog, LogLevel, LoggerBase

ERROR_MSG = 'msg'
RETURN_VALUE = 'ret1'


@pytest.fixture
def backend_mock():
    logger_mock = mock.create_autospec(LoggerBase)
    return logger_mock


class FakeException(Exception):
    pass


class Test_log_exception(object):
    def test_if_logger_is_called_for_loggin_exception(self, backend_mock):
        logger = ULog(logger=backend_mock, log_level=LogLevel.Debug)

        exception = FakeException()

        @logger.log_exception(msg=ERROR_MSG)
        def myfunc():
            raise exception

        with pytest.raises(FakeException):
            myfunc()

        backend_mock.exception.assert_called_once_with(LogLevel.Debug, ERROR_MSG, exception)

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

    def test_if_return_value_is_returned_when_there_is_no_exception(self, backend_mock):
        logger = ULog(logger=backend_mock, log_level=LogLevel.Debug)

        exception = FakeException()

        @logger.log_exception(ERROR_MSG, log_level=LogLevel.Debug)
        def myfunc():
            return RETURN_VALUE

        return_value = myfunc()

        assert backend_mock.exception.call_count == 0
        assert return_value == RETURN_VALUE


class Test_log_selected_params(object):
    def test_if_selected_paramet_is_logged(self, backend_mock):
        logger = ULog(logger=backend_mock, log_level=LogLevel.Debug)

        @logger.log_selected_params(msg=ERROR_MSG, params=('p1',))
        def f(p1, kw1=''):
            pass

        f('v1')

        backend_mock.log.assert_called_with(LogLevel.Debug, 'msg\n\tp1: v1')
        assert backend_mock.log.call_count == 1

    def test_if_value_is_returned(self, backend_mock):
        logger = ULog(logger=backend_mock, log_level=LogLevel.Debug)

        @logger.log_selected_params(msg=ERROR_MSG, params=('p1',))
        def f(p1, kw1=''):
            return RETURN_VALUE

        return_value = f('v1')

        assert return_value == RETURN_VALUE


class Test_log_params(object):
    def test_if_all_passed_params_are_logged(self, backend_mock):
        logger = ULog(logger=backend_mock, log_level=LogLevel.Debug)

        @logger.log_params(msg=ERROR_MSG)
        def f(p1, kw1=''):
            pass

        f('v1', 'v2')

        backend_mock.log.assert_called_with(LogLevel.Debug, 'msg\n\tp1: v1\n\tkw1: v2')
        assert backend_mock.log.call_count == 1

    def test_if_all_params_are_logged_except_default_values(self, backend_mock):
        logger = ULog(logger=backend_mock, log_level=LogLevel.Debug)

        @logger.log_params(msg=ERROR_MSG)
        def f(p1, kw1=''):
            pass

        f('v1')

        backend_mock.log.assert_called_with(LogLevel.Debug, 'msg\n\tp1: v1')
        assert backend_mock.log.call_count == 1

    def test_if_return_value_is_returned(self, backend_mock):
        logger = ULog(logger=backend_mock, log_level=LogLevel.Debug)

        @logger.log_params(msg=ERROR_MSG)
        def f(p1, kw1=''):
            return RETURN_VALUE

        return_value = f('v1')

        assert return_value == RETURN_VALUE

    def test_if_kwargs_are_logged(self, backend_mock):
        logger = ULog(logger=backend_mock, log_level=LogLevel.Debug)

        @logger.log_params(msg=ERROR_MSG)
        def f(p1, p2=''):
            pass

        f(p1='v1', p2='v2')

        call = backend_mock.log.call_args[0]
        logged_message = call[1]

        assert '\n\tp1: v1' in logged_message
        assert '\n\tp2: v2' in logged_message
        assert backend_mock.log.call_count == 1


class Test_log_return(object):
    def test_if_log_is_returned(self, backend_mock):
        logger = ULog(logger=backend_mock, log_level=LogLevel.Debug)

        @logger.log_return(msg=ERROR_MSG)
        def f():
            return RETURN_VALUE

        f()

        assert backend_mock.log.call_count == 1
        backend_mock.log.assert_called_with(LogLevel.Debug, 'msg%s' % RETURN_VALUE)

    def test_if_value_is_returned(self, backend_mock):
        logger = ULog(logger=backend_mock, log_level=LogLevel.Debug)

        @logger.log_return(msg=ERROR_MSG)
        def f():
            return RETURN_VALUE

        return_value = f()

        assert return_value == RETURN_VALUE
