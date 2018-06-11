#!/usr/bin/python
# coding=utf-8

from model.PlantModel import PlantData, PlantModel, Base, PlantType, sensor
from sqlalchemy import create_engine, or_, func
from sqlalchemy.orm import sessionmaker

# 初始化数据库连接:
engine = create_engine('mysql+pymysql://root:123456@192.168.2.153:3306/raspberry?charset=utf8')
# engine = create_engine('mysql+pymysql://root:123456@127.0.0.1:3306/raspberry?charset=utf8')
Session = sessionmaker(bind=engine)
# 如果表不存在则创建表
Base.metadata.create_all(engine)
# 只用一个session
session = Session()

# 获取没有植物生长模型的植物种类
def getActivePlantType():
    session.commit()
    plantModelIds = session.query(PlantModel.typeId).all()
    plantModelIds = [ plantModelId[0] for  plantModelId in plantModelIds ]
    result =session.query(PlantType).filter(~PlantType.id.in_(plantModelIds)).all()
    return result

def getAllPlantType():
    session.commit()
    return session.query(PlantType).all()

# 根据typeId或者type查询planttype
def getPlantType(planttype):
    session.commit()
    list = session.query(PlantType).filter(or_(PlantType.id==planttype.id,PlantType.type==planttype.type)).all()
    if len(list) > 1:
        return '输入的plantid与planttype不匹配'
    elif len(list) == 1:
        return list[0]
    else :
        return '无法查询到相应的植物类型'

def addPlantData(plantData):
    session.add(plantData)
    session.commit()



def deletePlantModelsByIds(ids):
    session.commit()
    result = session.query(PlantModel).filter(PlantModel.id.in_(ids)).all()
    for res in result:
        session.delete(res)
        session.commit()

def addPlantModel():
    plantModel = PlantModel()
    dbSession = Session()
    dbSession.add(plantModel)
    dbSession.commit()
    dbSession.close()

# 根据植物种类获取植物生长模型
def getPlantModel(plantType):
    session.commit()
    plantModel = session.query(PlantModel).filter(PlantModel.typeId == plantType).first()
    if plantModel :
        return plantModel
    else:
        print "未获取到植物的生长模型"

# 获取所有植物生长模型
def getAllPlantModel():
    # sqlalchemy 缓存机制很坑爹，如果不commit会导致查询到缓存中的内容
    session.commit()
    return session.query(PlantModel).all()

# 增加或修改植物生长模型
def addOrUpdatePlantModel(plantModel):
    result = session.query(PlantModel).filter(or_(PlantModel.id == plantModel.id,PlantModel.typeId == plantModel.typeId)).first()
    if result is not None:
        # 更新
        print 'update'
        plantModel.id = result.id
        plantModel.typeId = result.typeId
        session.merge(plantModel)
    else:
        print 'add'
        session.add(plantModel)
    session.commit()

# 删除植物生长模型
def delPlantModel(plantModel):
    result = session.query(PlantModel).filter(PlantModel.typeId == plantModel.typeId).first()
    session.delete(result)
    session.commit()

def addPlantModel():
    dbSession = Session()
    plantModel = PlantModel(typeId=5)
    dbSession.add(plantModel)
    dbSession.commit()
    dbSession.close()

# 获取所有传感器
def getAllSensors():
    session.commit()
    return session.query(sensor).all()

# 获取有效状态的传感器
def getActiveSensors():
    session.commit()
    return session.query(sensor).filter(sensor.isActive == True).all()

# 更新或增加传感器
def addOrUpdateSensor(s):
    # 先查询是否已存在
    result =session.query(sensor).filter(sensor.id == s.id).first()
    if result is not None:
        session.merge(s)
    else:
        session.add(s)
    session.commit()

def updateSensorState(s):
    result = session.query(sensor).filter(sensor.id == s.id).first()
    if result is not None:
        result.isActive = s.isActive
        session.merge(result)
        session.commit()
    else:
        return None

def rollback():
    session.rollback()