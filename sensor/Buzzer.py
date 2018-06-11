#!/usr/bin/python
# coding=utf-8
# 有源蜂鸣器
import time

import RPi.GPIO as GPIO

from common import RaspberryConfig

isRunning = True
def __init():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    GPIO.setup(RaspberryConfig._BUZZER_PIN, GPIO.OUT, initial=GPIO.HIGH)

def on(seconds=3):
    GPIO.output(RaspberryConfig._BUZZER_PIN, GPIO.LOW)
    time.sleep(seconds)
    close()

def close():
    GPIO.output(RaspberryConfig._BUZZER_PIN, GPIO.HIGH)


def beep(times,on_time=5,off_time=3):
    try:
        RaspberryConfig.setAttr('_BUZZER_ISRUNNING', True)
        __init()
        for i in range(0,times):
            on(on_time)
            time.sleep(off_time)
    finally:
        RaspberryConfig.setAttr('_BUZZER_ISRUNNING', False)

def test():
    try:
        beep(times=5)
    finally:
        GPIO.cleanup()
