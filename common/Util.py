#!/usr/bin/python
# coding=utf-8
import signal, functools

# 限制方法超时装饰器
import time


class TimeoutError(Exception): pass


def timeout(seconds, error_message="Timeout Error: the cmd 30s have not finished."):
    def decorated(func):
        result = ""

        def _handle_timeout(signum, frame):
            global result
            result = error_message
            raise TimeoutError(error_message)

        def wrapper(*args, **kwargs):
            global result
            signal.signal(signal.SIGALRM, _handle_timeout)
            signal.alarm(seconds)

            try:
                result = func(*args, **kwargs)
            finally:
                signal.alarm(0)
                return result
            return result

        return functools.wraps(func)(wrapper)

    return decorated

# 获取当前时间
def getCurrentTime(format='%Y-%m-%d %H:%M:%S'):
    timestruct = time.localtime(time.time())
    return time.strftime(format,time.localtime(time.time()))

