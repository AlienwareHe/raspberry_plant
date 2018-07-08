#!/usr/bin/python
# coding=utf-8
import multiprocessing

# 自定义变量全部使用_开头，格式为_varname
import os
import threading

_NAME= 'Raspberry'
_PLANTTYPE= ''
_PLANTTYPE_ID= ''

_PAUSE_TIME= 30

_DH11_PIN = 13
_YL69_MCP_PIN = 7
_BUZZER_PIN = 12


_CENTER_ISRUNNING = False
_BUZZER_ISRUNNING = False
_DH11_ISRUNNING = False
_YL69_ISRUNNING = False

# 蜂鸣器蜂鸣周期与持续时间
_BUZZER_periods = 3
_BUZZER_time = 10

class global_var:
    BUZZER_WORK_STATE = True

def get_buzzer_work_satate():
    return global_var.BUZZER_WORK_STATE

def set_buzzer_work_satate(value = False):
    global_var.BUZZER_WORK_STATE = value

# print dir()
import sys
# print type(sys.modules[__name__])
# print vars()
# setattr(sys.modules[__name__],'NAME','aaa')
# print NAME

def setAttr(key,value):
    setattr(sys.modules[__name__],key,value)

def getAllStr():
    list = dir(sys.modules[__name__])
    values = {}
    for key in list:
        if key.startswith('_') and not key.startswith('__') and not key.endswith('__'):
            values[key] = getattr(sys.modules[__name__],key)
    return values

def getAttr(key):
    return getattr(sys.modules[__name__],key)

def getProjectPath():
    return os.path.abspath(os.path.join(os.path.dirname(__file__),os.path.pardir))
