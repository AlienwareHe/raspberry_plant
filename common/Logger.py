# coding=utf-8

import logging

from common import RaspberryConfig


def getLogger(loggerName, loggerLevel=logging.INFO, loggerFile=''
              , formatter='%(asctime)s - %(levelname)s - %(message)s'):
    logger = logging.getLogger(loggerName)
    logger.setLevel(loggerLevel)

    # 日志文件handler,日志文件目录默认为工程目录下logs文件夹
    if not loggerFile:
        loggerFile = RaspberryConfig.getProjectPath() + '/logs/' + loggerName + '.logs'
    print loggerFile
    handler = logging.FileHandler(loggerFile,mode='w')
    handler.setLevel(loggerLevel)

    # 控制台handler
    console = logging.StreamHandler()
    console.setLevel(loggerLevel)

    handler.setFormatter(formatter)
    console.setFormatter(formatter)

    logger.addHandler(handler)
    logger.addHandler(console)
    return logger
