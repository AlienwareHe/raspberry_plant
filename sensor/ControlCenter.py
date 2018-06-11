#!/usr/bin/python
# coding=utf-8
import threading
import time

from common import Util, RaspberryConfig, Logger
from dataanalysis import DataUtil
from dataanalysis.DataUtil import CompareResult, ResultEnum
from dh11 import DH11
from model import DBUtil
from sensor import Buzzer
from sensor.GY30 import GY30
from sensor.camera import camera
from yl69 import YL69
import RPi.GPIO as GPIO

# 中控中心
from model.PlantModel import PlantData

sensorList = set()

# logger = Logger.getLogger(__name__)

# 循环读取传感器数据(没有加超时限制)
def run():
    print('传感器数据采集进程已启动')
    RaspberryConfig.setAttr('_CENTER_ISRUNNING',True)
    while RaspberryConfig._CENTER_ISRUNNING:
        getAndCompareAll()
        time.sleep(RaspberryConfig._PAUSE_TIME)


def stop():
    RaspberryConfig.setAttr('_CENTER_ISRUNNING',False)
    # 清空传感器列表
    try:
        sensorList.clear()
    except Exception,e:
        print('传感器正在读取中...已终止')
    print('已设置中控状态为停止')




def addSensor(sensor):
    sensorList.add(sensor)

def removeSensor(sensor):
    sensorList.remove(sensor)

# 获取所有传感器数据并与生长模型比较
def getAndCompareAll():
    # 从传感器中获取所有传感器数据
    plantData = PlantData()
    for sensor in sensorList:
        sensor.read(plantData)

    if not RaspberryConfig._PLANTTYPE:
        print '该次检测无植物类型设定，不进行比较'
        return plantData

    # 持久化植物生长数据
    DBUtil.addPlantData(plantData)
    # 与植物生长模型比较
    # todo 从数据库中获取植物生长模型,目前根据植物种类获取
    plantModel = getPlantModelByPlantType()
    compareResult = DataUtil.compare(plantData, plantModel)
    # 处理比较后的结果
    doSthForCompareResult[compareResult.result_code]()
    detail = ''
    for key in compareResult.result:
        result = compareResult.result[key]
        detail += key+result.__str__()+'\r\n'

    result = '{} :本次读取植物环境数据为：{},结果为{}\r\n具体信息:{}'.format(Util.getCurrentTime(), plantData.__str__()
                                                          , ResultEnum[compareResult.result_code], detail)
    print(result)
    print('-----------------------------')
    return result

__BUZZERLOCK = threading.Lock()
def forDanger():
    print 'Warning!!,植物生长环境不符合生长模型，将启动蜂鸣器'
    # 开启新的进程处理蜂鸣器，因为蜂鸣器可能会导致阻塞
    global __BUZZERLOCK
    try:
        if  __BUZZERLOCK.acquire(False) and not RaspberryConfig._BUZZER_ISRUNNING:
            print '抢到了蜂鸣锁并且没有正在运行的蜂鸣器,启动中...'
            t = threading.Thread(target=Buzzer.beep,args=(3,))
            t.start()
        else:
            print '当前蜂鸣器已在工作'
    finally:
        __BUZZERLOCK.release()

def forSafe():
    pass


def forDataNull():
    pass


def test():
    pass

doSthForCompareResult = {
    CompareResult.DANGER: forDanger,
    CompareResult.SAFE: forSafe,
    CompareResult.DATA_IS_NULL: forDataNull,
    'TEST': test
}


# 获取植物生长模型
def getPlantModelByPlantType():
    if RaspberryConfig._PLANTTYPE_ID:
        return DBUtil.getPlantModel(RaspberryConfig._PLANTTYPE_ID)
    else:
        print '请先设置所需要采集的植物类型'
        return None


def getAirTempHum():
    return DH11().readData()

def getSoilHum():
    plantData = PlantData()
    plantData =  YL69().read(plantData)
    return plantData.soilHumidity

def getPic(name = ''):
    plantData = PlantData()
    camera().read(plantData,name)
    return plantData.picture

def getLight():
    plantData = PlantData()
    GY30().read(plantData)
    return plantData.lightIntensity

def initalAndRun():
    GPIO.setmode(GPIO.BOARD)

    loadActiveSensors()
    # 如果已经有运行中的中控中心，则不处理
    if RaspberryConfig._CENTER_ISRUNNING:
        return '当前正在运行'
    t = threading.Thread(target=run)
    # 使用setDaemon让子线程和主线程一起销毁，但为了让主线程接收到Ctrl+C中止信号，主线程不采用join而采取无线循环的方式。
    t.setDaemon(True)
    t.start()
    print('主线程继续')

def loadActiveSensors():
    # 从数据库读取
    sensors = DBUtil.getActiveSensors()
    # 创建并添加传感器
    for sensor in sensors:
        try:
            instance = eval(sensor.class_name + '()')
            addSensor(instance)
        except Exception, e:
            print e