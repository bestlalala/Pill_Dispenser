import RPi.GPIO as G
import sys
import signal

G.setmode(G.BCM)


def signal_handler(signal, frame):
    print('process stop')
    p.stop()
    G.cleanup()
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)


SOUND = 21
MOTION_IN = 3
SERVO = 2

scale = [131, 147, 165, 175, 196, 220, 247, 262, 294, 330, 350, 392, 440, 494, 523, 124]    # 음계
servo_min_duty = 3
servo_max_duty = 12

G.setup(SOUND, G.OUT)
G.setup(MOTION_IN, G.IN)
G.setup(SERVO, G.OUT)

p = G.PWM(SOUND, 100)
PWM_RC = G.PWM(SERVO, 50)
