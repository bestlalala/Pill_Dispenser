import time
from GPIO_setup import *

# hand + ServoMotor
G.setmode(G.BCM)
G.setup(MOTION_IN, G.IN)
G.setup(SERVO, G.OUT)


def front():
   print("going front")
   set_servo_degree(52)
   time.sleep(0.5)


def center():
    print("going back")
    set_servo_degree(2)
    time.sleep(1.5)


def set_servo_degree(degree) :
    if degree > 180 :
        degree = 180
    elif degree < 0 :
        degree = 0
    duty = servo_min_duty + (degree*(servo_max_duty-servo_min_duty)/180.0)
    PWM_RC.ChangeDutyCycle(duty)


def setting_prox(num):  # 약 개수 받기
    print("setting_prox start", num)
    PWM_RC.start(45)

    for i in range(num):
        while True:
            if not G.input(MOTION_IN):
                front()
                center()
                break
            else:
                time.sleep(1)
