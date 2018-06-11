#coding=utf-8

from picamera import PiCamera
import time

from common import Util, RaspberryConfig, QiniuUploadUtil
from sensor.Sensor import Sensor

PIC_SUFFIX = '.jpg'
VIDEO_SUFFIX = '.mpeg'
piccamera = PiCamera()
piccamera.resolution = (1024, 768)
piccamera.start_preview()
filepath = RaspberryConfig.getProjectPath()+'/pics/'
# Camera warm-up time
time.sleep(2)

class camera(Sensor):

    def __init__(self,name='camera', type='camera'):
        super(camera, self).__init__(name, type)


    def read(self,plantData,name = ''):
        print('摄像头工作中...')
        # 获取图片
        filename = capturePic(name)
        # 联网状态下上传至七牛云,若断网则无法上传
        result = QiniuUploadUtil.store(filepath+filename,filename)
        # 保存七牛云外链或者本地路径至plantData
        if result.ret:
            plantData.picture = QiniuUploadUtil.assemblePicUrl(filename)
        else:
            plantData.picture = filepath+filename

# 截取图片保存为文件,文件默认保存路径为项目路径根目录下pic文件夹
def capturePic(filename=''):
    # 生成文件名(planttype+timestamp.jpg)
    if not filename :
        prifex = Util.getCurrentTime('%Y%m%d%H%M%S_')
        filename = prifex + RaspberryConfig._PLANTTYPE + PIC_SUFFIX

    piccamera.capture(filepath+filename)
    return filename

# 截取图片保存至流
def captureStream(outputstream):
    piccamera.capture(outputstream, 'jpeg')

# 获取视频保存为文件
def recordVideo(time=10,filename = ''):
    if not filename:
        prifex = Util.getCurrentTime('%Y%m%d%H%M%S_')
        filename = prifex + RaspberryConfig._PLANTTYPE + VIDEO_SUFFIX

    piccamera.resolution = (640, 480)
    piccamera.start_recording(filename)
    piccamera.wait_recording(time)
    piccamera.stop_recording()

