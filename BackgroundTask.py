import time


def alarm_start(c):
    c.acquire()
    print("알람 시작")
    for i in range(5):
        print(f"thread_3 is running {i}")
        time.sleep(0.1)
    print("the third thread ends")
    c.notify()
    c.release()


