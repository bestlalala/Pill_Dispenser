import RPi.GPIO as G
import time
import signal
import sys
from Alarm_piezo import *
from Yaknawa2 import *


#스레드1
def alarm_start(c):
    c.acquire()
    print("알람 시작")
    alarm_play(1)
    print("alarm_start thread ends")
    c.notify()
    c.release()


#스레드2
def activate_prox(c, pill_cnt):
    c.acquire()
    print("근접 센서 활성화 스레드 시작")
    setting_prox(pill_cnt)
    print("activate_prox thread ends")
    c.notify()
    c.release()
