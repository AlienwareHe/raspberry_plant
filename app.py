# -*- coding: utf-8 -*-
# 创建应用
import json
import re
import threading
import traceback

from flask import Flask, jsonify, render_template, request, url_for, redirect, abort
from flask_bootstrap import Bootstrap

from common import RaspberryConfig
from model import DBUtil
from model.JsonSchema import DHT11ResultSechema, SensorSechema, PlantModelDTO, PlantModelSchema, PlantTypeSchema
from model.PlantModel import PlantType, sensor, PlantModel
from sensor import ControlCenter

app = Flask(__name__)
# 加载配置文件
app.config.from_object('RaspberryConfig')
app.config['JSON_AS_ASCII'] = False
app.config['BOOTSTRAP_SERVE_LOCAL'] = True
Bootstrap(app)


# lock
controlcenter_lock = threading.Lock()

@app.route('/', methods=['GET'])
def hello():
    return redirect('/docs')


@app.route('/api/config',methods=['GET'])
def config():
    """
    查看树莓派所有配置
    :return: JSON字符串
    """
    return jsonify(RaspberryConfig.getAllStr())

@app.route('/config',methods=['GET'])
def listConfig():
    """
    树莓派配置列表页
    :return: html
    """
    configs = RaspberryConfig.getAllStr()
    return render_template('config.html',config = configs)

@app.route('/api/config/<key>/<value>',methods=['GET','PUT','POST'])
def updateConfig(key,value):
    """
    修改树莓派配置
    :param key: 将要修改的配置属性键值
    :param value: 将要修改的配置属性值
    :return: 修改后的树莓派配置
    """
    # todo 对key和value需要验证
    RaspberryConfig.setAttr(key, value)
    return '修改成功，key={},value={}'.format(key, RaspberryConfig.getAttr(key))

# 传感器部分
@app.route('/api/sensors', methods=['GET'])
def listSensors():
    """
    列出树莓派支持的所有传感器
    :return: list
    """
    sensors = DBUtil.getAllSensors()
    schema = SensorSechema()
    result = schema.dump(sensors,many=True)
    return jsonify(result)

@app.route('/sensors',methods=['GET'])
def sensors():
    return render_template('sensors.html')

@app.route('/api/sensors/<sensorId>/<status>')
def updateSensor(sensorId,status):
    """
    修改传感器状态
    :param sensorId: 传感器ID
    :param status:  修改的状态
    :return:
    """
    if status == 'false':
        status = False
    elif status == 'true':
        status = True

    sens = sensor(isActive=status)
    sens.id = sensorId
    try:
        # 数据库修改状态
        DBUtil.updateSensorState(sens)
        # 重新加载内存传感器列表
        ControlCenter.loadActiveSensors()
        return '修改成功'
    except Exception,e:
        DBUtil.rollback()
        return e.message

@app.route('/api/light',methods=['GET','POST'])
def getLight():
    return jsonify({"light":ControlCenter.getLight()})

@app.route('/api/sensor/soilHum',methods=['GET','POST'])
def getSoilHum():
    """
    获取土壤湿度
    :return: {'soilHum': 12}
    """
    soilhum = ControlCenter.getSoilHum()
    result = {}
    result['soilHum'] = soilhum
    return jsonify(result)

@app.route('/api/sensor/camera/<filename>')
def getPic(filename):
    """
    获取植物当前图像
    :param filename: 图像文件名
    :return:
    """
    return jsonify({"pic":ControlCenter.getPic(filename)})

def getLight():
    """
    获取植物当前光照情况
    :return:
    """
    return jsonify({'light':ControlCenter.getLight()})

@app.route('/api/sensor/airTempHum', methods=['GET'])
def getAirTempHum():
    """
    获取空气温度和湿度
    :return: {
                 "error_code": 0,
                 "humidity": 39,
                 "temperature": 21
             }
    """
    schema = DHT11ResultSechema()
    result = ControlCenter.getAirTempHum()
    result = schema.dump(result)
    return jsonify(result)

@app.route('/api/sensor/all', methods=['GET'])
def getAllSensorData():
    """
    获取一次全量传感器数据并与生长模型比较
    :return: {time} :本次读取植物环境数据为：{data}，结果为{compare_result}
    """
    return jsonify(ControlCenter.getAndCompareAll())

# 植物生长模型
@app.route('/plantmodel',methods=['GET','POST'])
def plantModelIndex():
    return render_template('plantmodel.html')

@app.route('/api/plantmodel',methods=['GET'])
def getAllPlantModel():
    """
    获取所有植物生长类型列表
    :return:
    """
    plantmodels = DBUtil.getAllPlantModel()
    print '查询出{}条植物生长类型'.format(len(plantmodels))
    plantmodelDtos = [PlantModelDTO().convertFromPlantModel(plantmodel) for plantmodel in plantmodels ]
    result = PlantModelSchema().dump(plantmodelDtos,many=True)
    return jsonify(result)

@app.route('/api/plantmodel',methods=['DELETE'])
def delPlantModelByIds():
    """
    根据植物生长模型id列表删除植物生长模型
    :param: {delIds:[]}
    :return:
    """
    # 接收参数为数组时，需要先将参数通过json转化
    delIds = request.form.get("delIds")
    delIds = json.loads(delIds)
    print delIds
    DBUtil.deletePlantModelsByIds(delIds)
    return '删除成功'

@app.route('/addPlantModel.html')
def renderAddPlantModel():
    return render_template('addPlantModel.html')

@app.route('/api/plantmodel',methods=['POST'])
def addPlantModel():
    """
    添加植物生长模型
    :return:
    """
    # 组装对象
    plantModel = PlantModel()
    plantModel.typeId = request.form.get('typeId')
    print request.values
    print request.values.get('light_low',default='0')
    plantModel.lightIntensity_low = request.form.get('light_low',default='0')
    plantModel.lightIntensity_high = request.form.get('light_high',default='0')
    plantModel.soilHumidity_low = request.form.get('soilhum_low',default='0')
    plantModel.soilHumidity_high = request.form.get('soilhum_high',default='0')
    plantModel.airTemprature_high = request.form.get('airTemp_high',default='0')
    plantModel.airTemprature_low = request.form.get('airTemp_low',default='0')
    plantModel.airHumidity_low = request.form.get('airHum_low',default='0')
    plantModel.airHumidity_high = request.form.get('airHum_high',type=str,default='0')
    plantModel.CO2concetration_low = request.form.get('co2_low',type=str,default='0')
    plantModel.CO2concetration_high = request.form.get('co2_high',default='0')
    try:
        DBUtil.addOrUpdatePlantModel(plantModel)
        return '添加成功'
    except Exception,e:
        print e
        DBUtil.rollback()
        return 'false'

@app.route('/api/editPlantmodel',methods=['POST'])
def updatePlantModel():
    """
    更新植物生长模型，请求content-type必须为application/json
    :return:
    """
    if not request.json:
        abort(400)
    jsonData = request.data
    # loads方法接受一个json string 而load方法接受一个字典
    schema = PlantModelSchema()
    plantModelDto = schema.loads(jsonData,partial=True)
    plantModel = plantModelDto.convertToPlantModel()
    try:
        DBUtil.addOrUpdatePlantModel(plantModel)
        return "更新成功"
    except Exception,e:
        DBUtil.rollback()
        return "更新失败"

# 植物类型
@app.route('/api/planttypes',methods=['GET'])
def getPlantTypes():
    """
    获取所有植物类型，参数isAll为True代表获取所有，否则获取没有对应植物生长模型的植物类型

    :return:
    """
    isAll = request.args.get('isAll')
    if isAll == "True":
        result = DBUtil.getAllPlantType()
    else:
        result = DBUtil.getActivePlantType()
    result = PlantTypeSchema().dump(result,many=True)
    return jsonify(result)

@app.route('/api/run', methods=['GET'])
# 开启或关闭控制中心，on/off
def controlCenter():
    """
    开启或关闭控制中心，mode=on代表开启，默认为on，若开启还需plantTypeId参数或者plantType参数
    :return: 开启成功或失败提示
    """
    mode = request.args.get('mode', default='on')
    # 加锁
    global controlcenter_lock
    if mode == 'on' and controlcenter_lock.acquire():
        try:
            plantTypeId = request.args.get('plantTypeId')
            type = request.args.get('plantType')
            if plantTypeId or type:
                # validate plantType is exist
                plantType = PlantType(plantTypeId, type)
                res = DBUtil.getPlantType(plantType)
                if isinstance(res, PlantType):
                    RaspberryConfig._PLANTTYPE_ID = res.id
                    RaspberryConfig._PLANTTYPE = res.type
                else:
                    return '输入正确的ID或TYPE'

            else:
                return '至少输入树莓派检测的植物类型或ID'

            if not RaspberryConfig._CENTER_ISRUNNING:
                RaspberryConfig.setAttr('_ISRUNNING', True)
                ControlCenter.initalAndRun()
            else:
                return '当前已经正在运行'
        finally:
            # 释放锁
            controlcenter_lock.release()
        return '传感器数据采集进程正在启动'
    elif mode == 'off':
        ControlCenter.stop()
        return '传感器数据采集进程已关闭'

@app.route('/api/runstate',methods=['GET','POST'])
def getRunState():
    """
    获取控制中心运行状态
    :return:
    """
    return str(RaspberryConfig._CENTER_ISRUNNING)


# API部分
def get_app():
    return app


def get_api_map():
    """Search API from rules, if match the pattern then we said it is API."""
    for rule in app.url_map.iter_rules():
        if re.search(r'/api/.+', str(rule)):
            yield str(rule), rule.endpoint

@app.route('/docs',methods=['GET'])
def index():
    """List all API to this page, api_map contains each api url + endpoint."""
    api_map = sorted(list(get_api_map()))
    index_url = url_for('hello', _external=True)
    api_map = [(index_url + x[0][1:] + '/', x[1]) for x in api_map]
    return render_template('api/api_index.html', api_map=api_map)

@app.route('/docs/<endpoint>',methods=['GET','POST'])
def docs(endpoint):
    """Document page for an endpoint."""
    api = {
        'endpoint': endpoint,
        'methods': [],
        'doc': '',
        'url': '',
        'name': ''
    }

    try:
        func = get_app().view_functions[endpoint]

        api['name'] = _get_api_name(func)
        api['doc'] = _get_api_doc(func)
        print api['doc']
        for rule in get_app().url_map.iter_rules():
            if rule.endpoint == endpoint:
                api['methods'] = ','.join(rule.methods)
                api['url'] = str(rule)

    except:
        api['doc'] = 'Invalid api endpoint: "{}"!'.format(endpoint)

    return render_template('api/api_docs.html', api=api)


def _get_api_name(func):
    """e.g. Convert 'do_work' to 'Do Work'"""
    words = func.__name__.split('_')
    words = [w.capitalize() for w in words]
    return ' '.join(words)


def _get_api_doc(func):
    if func.__doc__:
        return func.__doc__
    else:
        return 'No doc found for this API!'


if __name__ == "__main__":
    print('主线程启动')
    # Watcher()
    app.run('0.0.0.0')
