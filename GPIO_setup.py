import RPi.GPIO as G
import sys
import signal
import time

scale = [131, 147, 165, 175, 196, 220, 247, 262, 294, 330, 350, 392, 440, 494, 523, 124]  # 음계
servo_min_duty = 3
servo_max_duty = 12

SOUND = 21
MOTION_IN = 3
SERVO = 2


G.setmode(G.BCM)


def signal_handler(signal, frame):
    print('process stop')
    p.stop()
    G.cleanup()
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)


G.setup(SOUND, G.OUT)
G.setup(MOTION_IN, G.IN)
G.setup(SERVO, G.OUT)


p = G.PWM(SOUND, 100)
PWM_RC = G.PWM(SERVO, 50)

#알람
def freeze():
    p.ChangeDutyCycle(0)
    time.sleep(0.15)
    p.ChangeDutyCycle(10)


def note8(i):
    p.ChangeFrequency(scale[i])
    time.sleep(0.15)
    freeze() # 8분음표


def note4(i):
    p.ChangeFrequency(scale[i])
    time.sleep(0.3)
    freeze() # 4분음표


def note3(i):
    p.ChangeFrequency(scale[i])
    time.sleep(0.45)
    freeze() # 3분음표_summer


def note3_2(i):
    p.ChangeFrequency(scale[i])
    time.sleep(0.9)
    freeze() # 3분음표_cry


def note2(i):
    p.ChangeFrequency(scale[i])
    time.sleep(0.6)
    freeze() # 2분음표


def play_summer():
    note8(4)  # 솔
    note8(7)  # 도
    note8(8)  # 레
    note8(9)  # 미
    note4(8)  # 레
    note8(7)  # 도
    note3(7)  # 도
    freeze()
    note8(4)  # 솔
    note8(7)  # 도
    note8(8)  # 레
    note8(9)  # 미
    note4(8)  # 레
    note8(7)  # 도
    note3(8)  # 레
    note3(9)  # 미
    note3(9)  # 미
    freeze()


def play_cry():
    note8(2)  # 미
    note8(3)  # 파
    note4(4)  # 솔
    note4(4)  # 솔
    freeze()
    note8(5)  # 라
    note8(6)  # 시
    note4(7)  # 도
    note4(7)  # 도
    freeze()
    note8(2)  # 미
    note8(3)  # 파
    note8(4)  # 솔
    note8(4)  # 솔
    note8(4)  # 솔
    note4(4)  # 솔
    note8(5)  # 라
    note8(4)  # 솔
    note8(3)  # 파
    note8(3)  # 파
    note2(3)  # 파
    note4(2)
    note4(4)
    note4(0)
    note4(1)
    note4(3)
    note4(3)
    note4(15)
    note3_2(0)


def alarm_play(num):
    p.start(100)
    p.ChangeDutyCycle(10)
    if (num%2) == 0:
        play_summer()
    elif (num%2) == 1:
        play_cry()
    p.stop()


#근접센서
def front():
    print("going front")
    set_servo_degree(52)
    time.sleep(0.5)


def center():
    print("going back")
    set_servo_degree(2)
    time.sleep(1.5)


def set_servo_degree(degree):
    if degree > 180:
        degree = 180
    elif degree < 0:
        degree = 0
    duty = servo_min_duty + (degree * (servo_max_duty - servo_min_duty) / 180.0)
    PWM_RC.ChangeDutyCycle(duty)


def setting_prox(num):  # 약 개수 받기

    PWM_RC.start(45)

    for i in range(num):
        while True:
            if not G.input(MOTION_IN):
                front()
                center()
                break
            else:
                time.sleep(0.5)
