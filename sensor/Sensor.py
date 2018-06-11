#!/usr/bin/python
# coding=utf-8

# 所有传感器的父类
from abc import ABCMeta,abstractmethod
class Sensor(object):

    # 子类重写了init方法时便不会调用父类的init方法，因此子类需要显示调用该方法
    def __init__(self,name,type):
        self.sensorName = name
        self.sensorType = type

    @abstractmethod
    # 读取一次数据
    def read(self,plantData):pass

    # 循环读取数据