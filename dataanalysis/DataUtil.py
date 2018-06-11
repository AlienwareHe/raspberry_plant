#!/usr/bin/python
# encoding=utf-8
from intervals import IntInterval

ResultEnum = {
    1:'符合标准',
    2:'不符合标准，警告！！',
    3:'为空',
    4:'异常'
}


class CompareResult():
    """
    植物生长模型与实时生长数据的比较结果
    """
    SAFE = 1
    DANGER = 2
    DATA_IS_NULL = 3
    ERROR = 4

    def __init__(self,result_code=SAFE,result={}):
        self.result_code = result_code
        self.result = result

    def __str__(self):
        return '结果为{},具体结果为{}'.format(self.result_code,self.result)

class SensorResult():
    """
    每个传感器的数据比较结果
    :param
        result Boolean 比较结果
        originData String 原始数据
        standardData String 标准数据
        detail String 比较详细信息
        advice String 指导信息
    """

    def __init__(self,result,originData,standardData ,detail = '',advice = '无意见，结果符合标准'):
        self.result = result
        self.detail = detail
        self.advice = advice
        self.originData = originData
        self.standardData = standardData

    def __str__(self):
        return '测量数据为{},标准数据为{},指导意见:{}'.format(self.originData,self.standardData,self.advice)

def compare(plantData,plantModel):
        if not plantModel or not plantData:
            print '数据不能为空，请检查数据'
            return CompareResult(CompareResult.DATA_IS_NULL)

        result = dict()
        result['soilHum'] = compareSoilHum(plantData.soilHumidity,plantModel)
        result['airTemp'] = compareAirTemp(plantData.airTemperature,plantModel)
        result['airHum'] = compareAirHum(plantData.airHumidity,plantModel)
        result['light'] = compareLight(plantData.lightIntensity,plantModel)
        result['co2'] = SensorResult(True, originData='0', standardData='0-0')

        #todo 与植物生长模型比较
        if result['co2'].result and result['airTemp'].result and result['airHum'].result and result['soilHum'].result and result['light'].result:
            return CompareResult(CompareResult.SAFE,result)
        else:
            return CompareResult(CompareResult.DANGER,result)


def compareAirTemp(airTemp,plantModel):
    """
    比较空气温度
    :param airTemp: 实时数据
    :param plantModel: 标准生长模型
    :return: SensorResult
    """
    if not plantModel.airTemprature_low or not plantModel.airTemprature_high:
        return SensorResult(True,airTemp,standardData='0-0',advice='标准生长模型为空')

    ret = airTemp in IntInterval.closed(plantModel.airTemprature_low,plantModel.airTemprature_high)
    if ret:
        return SensorResult(True,airTemp,str(plantModel.airTemprature_low)+'-'+str(plantModel.airTemprature_high))
    else:
        # todo 给出指导意见
        if airTemp - plantModel.airTemprature_low < 0 :
            advice = "当前温度为{},标准温度为{}，建议至少{}温度{}".format(airTemp,plantModel.airTemprature_low,'上调',
                                                       plantModel.airTemprature_low-airTemp)
        else:
            advice = "当前温度为{},标准温度为{}，建议至少{}温度{}".format(airTemp, plantModel.airTemprature_high, '下调',
                                                       airTemp - plantModel.airTemprature_high)
        return SensorResult(False,airTemp,str(plantModel.airTemprature_low)+'-'+str(plantModel.airTemprature_high),advice=advice)


def compareSoilHum(soilHum, plantModel):
    if not plantModel.soilHumidity_low or not plantModel.soilHumidity_high:
        return SensorResult(True, soilHum, '0', '0', '标准生长模型为空')

    ret = soilHum in IntInterval.closed(plantModel.soilHumidity_low, plantModel.soilHumidity_high)
    if ret:
        return SensorResult(True, soilHum, str(plantModel.soilHumidity_low )+ '-' + str(plantModel.soilHumidity_high))
    else:
        # todo 给出指导意见
        if soilHum - plantModel.soilHumidity_low < 0:
            advice = "当前土壤湿度为{},标准土壤湿度为{}，建议至少{}土壤湿度{}".format(soilHum, plantModel.soilHumidity_low, '上调',
                                                       plantModel.soilHumidity_low - soilHum)
        else:
            advice = "当前土壤湿度为{},标准土壤湿度为{}，建议至少{}土壤湿度{}".format(soilHum, plantModel.soilHumidity_high, '下调',
                                                       soilHum - plantModel.soilHumidity_high)
        return SensorResult(False, soilHum, str(plantModel.soilHumidity_low) + '-' + str(plantModel.soilHumidity_high),
                            advice=advice)

def compareLight(light, plantModel):
    if not plantModel.lightIntensity_low or not plantModel.lightIntensity_high:
        return SensorResult(True, light, '0', '0', '标准生长模型为空')

    ret = light in IntInterval.closed(plantModel.lightIntensity_low, plantModel.lightIntensity_high)
    if ret:
        return SensorResult(True, light, str(plantModel.lightIntensity_low) + '-' + str(plantModel.lightIntensity_high))
    else:
        # todo 给出指导意见
        if light - plantModel.lightIntensity_low < 0:
            advice = "当前光照强度为{},标准光照强度为{}，建议至少{}光照强度{}".format(light, plantModel.lightIntensity_low, '上调',
                                                               plantModel.lightIntensity_low - light)
        else:
            advice = "当前光照强度为{},标准光照强度为{}，建议至少{}光照强度{}".format(light, plantModel.lightIntensity_high, '下调',
                                                               light - plantModel.lightIntensity_high)
        return SensorResult(False, light, str(plantModel.lightIntensity_low) + '-' + str(plantModel.lightIntensity_high),
                            advice=advice)

def compareAirHum(airHum, plantModel):
    if not plantModel.airHumidity_low or not plantModel.airHumidity_high:
        return SensorResult(True, airHum, '0', '0', '标准生长模型为空')

    ret = airHum in IntInterval.closed(plantModel.airHumidity_low, plantModel.airHumidity_high)
    if ret:
        return SensorResult(True, airHum, str(plantModel.airHumidity_low) + '-' + str(plantModel.airHumidity_high))
    else:
        # todo 给出指导意见
        if airHum - plantModel.airHumidity_low < 0:
            advice = "当前光照强度为{},标准光照强度为{}，建议至少{}光照强度{}".format(airHum, plantModel.airHumidity_low, '上调',
                                                               plantModel.airHumidity_low - airHum)
        else:
            advice = "当前光照强度为{},标准光照强度为{}，建议至少{}光照强度{}".format(airHum, plantModel.airHumidity_high, '下调',
                                                               airHum - plantModel.airHumidity_high)
        return SensorResult(False, airHum, str(plantModel.airHumidity_low)+ '-' + str(plantModel.airHumidity_high),
                            advice=advice)