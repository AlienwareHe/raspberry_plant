# coding=utf-8
from marshmallow import Schema, fields, post_load

from model.PlantModel import PlantModel


class DHT11ResultSechema(Schema):
    error_code = fields.Int()
    temperature = fields.Int()
    humidity = fields.Int()

class SensorSechema(Schema):
    id = fields.Int()
    name = fields.String()
    class_name = fields.String()
    nickname = fields.String()
    isActive = fields.String()

class PlantModelSchema(Schema):
    id = fields.Int()
    type = fields.String(20)
    airtemp = fields.String(20)
    airhum = fields.String(20)
    soilhumi = fields.String(20)
    light = fields.String(20)
    growStatus = fields.String(20)

    # 将dict转化为对象需要自己实现，然后加上注解
    @post_load()
    def make(self,data):
        return PlantModelDTO(**data)

class PlantTypeSchema(Schema):
    id = fields.Int()
    type = fields.String(20)

class PlantModelDTO():

    def convertFromPlantModel(self,plantModel):
        self.id = plantModel.id
        self.type = plantModel.typeInfo.type
        self.airtemp = str(plantModel.airTemprature_low)+'~'+str(plantModel.airTemprature_high)
        self.airhum = str(plantModel.airHumidity_low) +'~' + str(plantModel.airHumidity_high)
        self.soilhumi = str(plantModel.soilHumidity_low)+'~'+str(plantModel.soilHumidity_high)
        self.light = str(plantModel.lightIntensity_low) +'~'+str(plantModel.lightIntensity_high)
        self.growStatus = plantModel.typeInfo.growStatus
        return self

    def __init__(self,id=-1,type='',airtemp='',airhum='',soilhumi='',light=''):
        self.id = id
        self.type = type
        self.airtemp = airtemp
        self.airhum = airhum
        self.soilhumi = soilhumi
        self.light = light



    def convertToPlantModel(self):
        plantModel = PlantModel()
        plantModel.id = self.id
        plantModel.airHumidity_low = self.airhum.split('~')[0]
        plantModel.airHumidity_high = self.airhum.split('~')[1]
        plantModel.airTemprature_low = self.airtemp.split('~')[0]
        plantModel.airTemprature_high = self.airtemp.split('~')[1]
        plantModel.soilHumidity_low = self.soilhumi.split('~')[0]
        plantModel.soilHumidity_high = self.soilhumi.split('~')[1]
        plantModel.lightIntensity_low = self.light.split('~')[0]
        plantModel.lightIntensity_high = self.light.split('~')[1]
        return plantModel