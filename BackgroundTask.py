import time


def alarm_start(c):
    c.acquire()
    print("알람 시작")
    for i in range(10):
        print(f"thread_3 is running {i}")
        time.sleep(1)
    print("alarm_start thread ends")
    c.notify()
    c.release()


def activate_prox(c):
    c.acquire()
    print("근접센서 활성화 스레드 시작")
    for i in range(5):
        print(f"thread_3 is running {i}")
        time.sleep(1)
    print("activate_prox thread ends")
    c.notify()
    c.release()
