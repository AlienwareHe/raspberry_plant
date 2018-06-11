#!/usr/bin/python
# -*- coding=utf-8 -*-
from sensor.Sensor import Sensor
import smbus



class GY30(Sensor):

    def __init__(self,name='GY30光强传感器',type='光照强度'):
        super(GY30,self).__init__(name,type)

    def read(self,plantData):
        print('GY-30光照传感器工作中...'),

        bus = smbus.SMBus(1)
        addr = 0x23
        data = bus.read_i2c_block_data(addr, 0x11)
        # 两位小数
        data = str(round((data[1] + (256 * data[0])) / 1.2,2))
        if not data:
            print('WARNING！光照强度传感器采集数据为0或空')
            plantData.lightIntensity = 0
            return
        plantData.lightIntensity = data
        print data
