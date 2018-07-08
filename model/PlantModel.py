#!/usr/bin/python
#coding=utf-8
from datetime import datetime

from sqlalchemy import Column, Integer, DateTime, Float, String, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

# 植物生长数据
class PlantData(Base):
    __tablename__ = 'plantinfo'

    id = Column('id',Integer,primary_key=True,autoincrement=True)
    plantID = Column('plantID',Integer)
    time = Column('time',DateTime,default=datetime.now())
    soilTemp = Column('soilTemp',Float)
    soilHumidity = Column('soilHum',Float)
    airTemperature = Column('airTemp',Float)
    airHumidity = Column('airHum',Float)
    lightIntensity = Column('light',Float)
    CO2concetration = Column('co2',Float)
    picture = Column('picture',String(50))
    video = Column('video',String(50))
    growStatusID = Column('growStatusID',Integer)

    def __init__(self, soilHumidity = False, airTemperature = 0, airHumidity = 0, lightIntensity = 0, CO2concetration = 0):
        self.soilHumidity = soilHumidity
        self.airTemperature = airTemperature
        self.airHumidity = airHumidity
        self.lightIntensity = lightIntensity
        self.CO2concetration = CO2concetration
        # for not null
        self.plantID = 1
        self.soilTemp = 0
        self.growStatusID = 1

    def __str__(self):
        return '土壤湿度：{},空气温度：{}，空气湿度：{}，光照强度：{}，二氧化碳浓度：{}'.format(self.soilHumidity, self.airTemperature, self.airHumidity, self.lightIntensity, self.CO2concetration)

# 植物生长模型，上下限
class PlantModel(Base):
    __tablename__ = 'plant_model'

    id = Column('id',Integer,primary_key=True,autoincrement=True)
    soilHumidity_high = Column('soilHumidity_high',Integer)
    soilHumidity_low = Column('soilHumidity_low',Integer)
    airTemprature_high = Column('airTemprature_high',Integer)
    airTemprature_low =Column('airTemprature_low',Integer)
    airHumidity_high = Column('airHumidity_high',Integer)
    airHumidity_low = Column('airHumidity_low',Integer)
    lightIntensity_high = Column('lightIntensity_high',Integer)
    lightIntensity_low = Column('lightIntensity_low',Integer)
    CO2concetration_high =Column('CO2concetration_high',Integer)
    CO2concetration_low = Column('CO2concetration_low',Integer)
    typeId = Column('typeid',Integer,ForeignKey('planttype.TypeID'))

    typeInfo = relationship("PlantType")

    def __init__(self,typeId=-1,soilHumidity_high=0,soilHumidity_low=0,airTemprature_high=0,airTemprature_low=0,airHumidity_high=0,
                 airHumidity_low=0,lightIntensity_high=0,lightIntensity_low=0,CO2concetration_high=0,CO2concetration_low=0):
        self.soilHumidity_high = soilHumidity_high
        self.soilHumidity_low = soilHumidity_low
        self.airTemprature_high = airTemprature_high
        self.airTemprature_low = airTemprature_low
        self.airHumidity_high = airHumidity_high
        self.airHumidity_low = airHumidity_low
        self.lightIntensity_high = lightIntensity_high
        self.lightIntensity_low = lightIntensity_low
        self.CO2concetration_high = CO2concetration_high
        self.CO2concetration_low = CO2concetration_low
        self.typeId = typeId

    def __str__(self):
        print '植物生长模型:空气温度{}，空气湿度{},土壤湿度{}，光照强度{}，co2浓度{}'.format(
                                                                    self.airTemprature_low + '--' +self.airTemprature_high,
                                                                    self.airHumidity_low + '--' + self.airHumidity_high,
                                                                    self.soilHumidity_low + '--' + self.soilHumidity_high,
                                                                    self.lightIntensity_low + '--' + self.lightIntensity_high,
                                                                    self.CO2concetration_low + '--' + self.CO2concetration_low)
# 植物类型
class PlantType(Base):
    __tablename__ = 'planttype'

    id = Column('TypeID',Integer,primary_key=True,autoincrement=True)
    type = Column('type',String(50))
    growStatus = Column('grow_status',String(50))

    def __init__(self,plantid='',planttype=''):
        self.id = plantid
        self.type = planttype
        self.growStatus = growStatus

class sensor(Base):
    __tablename__ = 'sensor'

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    name = Column('name',String(20))
    class_name = Column('class',String(20))
    nickname = Column('nickname',String(20))
    isActive = Column('active',Boolean)

    def __init__(self,name='',class_name='',nickname='',isActive=False):
        self.isActive = isActive
        self.class_name = class_name
        self.name = name
        self.nickname = nickname