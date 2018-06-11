#!/usr/bin/python
# coding=utf-8

import sys
import threading
from os import path

from common import RaspberryConfig
from Sensor import Sensor

# 将当前文件夹的母文件夹加入系统路径中
from sensor import MCP3008


lock = threading.Lock()

class YL69(Sensor):

    def __init__(self,name='soil temperature',type='temperature'):
        super(YL69,self).__init__(name,type)
        self.isRunning = True

    # 读取一次湿度电平
    # @timeout(5)
    def read(self,plantData):
        soilHumidity = self.readData()
        plantData.soilHumidity = soilHumidity

    def readData(self):
        print('YL69传感器工作中...')
        if lock.acquire():
            volts = MCP3008.readVolts(RaspberryConfig._YL69_MCP_PIN)
            soilHumidity = self.convertVoltsToHumi(volts)
            lock.release()
            return soilHumidity


    # todo  完善公式
    def convertVoltsToHumi(self,volts):
        humi = -20.622 * volts + 98
        return humi

if __name__ == "__main__":
    print('YL-63传感器开始读取')
    yl69 = YL69()
    yl69.read()