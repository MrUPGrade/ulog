# coding=utf-8
from __future__ import absolute_import

import pytest
import mock
import logging
from ulog import ULog, LogLevel

ERROR_MSG = 'msg'
RETURN_VALUE = 'ret1'


class FakeException(Exception):
    pass


@pytest.fixture
def python_logger():
    m = mock.MagicMock(spec=logging.Logger)
    return m


class TestULogLogException(object):
    def test_if_logger_is_called_for_loggin_exception(self, python_logger):
        logger = ULog(logger=python_logger)

        exception = FakeException()

        @logger.log_exception(msg=ERROR_MSG)
        def myfunc():
            raise exception

        with pytest.raises(FakeException):
            myfunc()

            python_logger.log.assert_called_once_with(40, ERROR_MSG, True)

    def test_if_the_same_log_level_is_loged(self, python_logger):
        logger = ULog(logger=python_logger)

        exception = FakeException()

        @logger.log_exception(ERROR_MSG, level=LogLevel.Debug)
        def myfunc():
            raise exception

        with pytest.raises(FakeException):
            myfunc()

        assert python_logger.log.call_count == 1

    def test_if_return_value_is_returned_when_there_is_no_exception(self, python_logger):
        logger = ULog(logger=python_logger)

        @logger.log_exception(ERROR_MSG, level=LogLevel.Debug)
        def myfunc():
            return RETURN_VALUE

        return_value = myfunc()

        assert python_logger.log.call_count == 0
        assert return_value == RETURN_VALUE


class TestLogArgs(object):
    def test_if_selected_paramet_is_logged(self, python_logger):
        logger = ULog(logger=python_logger)

        @logger.log_args(msg=ERROR_MSG, arguments=('p1',))
        def f(p1, kw1=''):
            pass

        f('v1')

        python_logger.log.assert_called_with(10, 'msg\np1: v1', exc_info=False)
        # assert python_logger.log.call_count == 1

    def test_if_value_is_returned(self, python_logger):
        logger = ULog(logger=python_logger)

        @logger.log_args(msg=ERROR_MSG, arguments=('p1',))
        def f(p1, kw1=''):
            return RETURN_VALUE

        return_value = f('v1')

        assert return_value == RETURN_VALUE

    def test_if_the_same_log_level_is_loged(self, python_logger):
        logger = ULog(logger=python_logger)

        @logger.log_args(msg=ERROR_MSG, arguments=('p1',), level=LogLevel.Debug)
        def f(p1, kw1=''):
            return RETURN_VALUE

        f('v1')

        assert python_logger.log.call_count == 1

    def test_if_all_passed_params_are_logged(self, python_logger):
        logger = ULog(logger=python_logger)

        @logger.log_args(msg=ERROR_MSG)
        def f(p1, kw1=''):
            pass

        f('v1', 'v2')

        python_logger.log.assert_called_with(LogLevel.Debug, 'msg\np1: v1\nkw1: v2', exc_info=False)
        assert python_logger.log.call_count == 1

    def test_if_all_params_are_logged_except_default_values(self, python_logger):
        logger = ULog(logger=python_logger)

        @logger.log_args(msg=ERROR_MSG)
        def f(p1, kw1=''):
            pass

        f('v1')

        python_logger.log.assert_called_with(LogLevel.Debug, 'msg\np1: v1', exc_info=False)
        assert python_logger.log.call_count == 1

    def test_if_return_value_is_returned(self, python_logger):
        logger = ULog(logger=python_logger)

        @logger.log_args(msg=ERROR_MSG)
        def f(p1, kw1=''):
            return RETURN_VALUE

        return_value = f('v1')

        assert return_value == RETURN_VALUE

    def test_if_kwargs_are_logged(self, python_logger):
        logger = ULog(logger=python_logger)

        @logger.log_args(msg=ERROR_MSG)
        def f(p1, p2=''):
            pass

        f(p1='v1', p2='v2')

        call = python_logger.log.call_args[0]
        logged_message = call[1]

        assert '\np1: v1' in logged_message
        assert '\np2: v2' in logged_message
        assert python_logger.log.call_count == 1


class Test_log_return(object):
    def test_if_log_is_returned(self, python_logger):
        logger = ULog(logger=python_logger)

        @logger.log_return()
        def f():
            return RETURN_VALUE

        f()

        assert python_logger.log.call_count == 1

        call = python_logger.log.call_args[0]

        logged_message = call[1]
        assert RETURN_VALUE in logged_message

        assert LogLevel.Debug == call[0]

    def test_if_value_is_returned(self, python_logger):
        logger = ULog(logger=python_logger)

        @logger.log_return(msg=ERROR_MSG)
        def f():
            return RETURN_VALUE

        return_value = f()

        assert return_value == RETURN_VALUE

    def test_if_the_same_log_level_is_loged(self, python_logger):
        logger = ULog(logger=python_logger)

        @logger.log_return(msg=ERROR_MSG, level=LogLevel.Debug)
        def f():
            return RETURN_VALUE

        f()

        assert python_logger.log.call_count == 1
