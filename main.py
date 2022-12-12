import tkinter as tk
import time
from UserInfo import *

global now
global bottle_num
global user_cnt
user_cnt = 0
global pill_info
global new_user

# main window
class DispenserApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title("Pill Dispenser")
        self.geometry("750x500")
        self.resizable(False, False)

        # 가장 기본적인 화면으로 container라는 이름으로 기본 프레임 선언.
        # 이 기본 프레임 위에 다른 프레임들이 쌓임
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, UserSetting, PutPill, AlarmSetting, AlarmCheck):
            page_name = F.__name__  # 각 class의 이름을 가져와서 저장
            frame = F(parent=container, controller=self)  # class의 _init_실행
            self.frames[page_name] = frame  # 각 class별 저장소에 각 class별 frame의 내용 저장

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")  # 각 프레임을 순서대로 화면에 출력

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()  # 요청된 page_name에 맞는 frame을 찾아서 tkraise() 함수로 맨 위에 올려 화면에 보이게 함.


# 메인 윈도우창 선언 끝

# 스택으로 쌓아서 보여줄 프레임 클래스들


# 1. 시계 프레임
class StartPage(tk.Frame):

    # 시계
    def clock(self):
        global now
        now = time.strftime("%H:%M:%S")
        self.clock_width.config(text=now)
        self.clock_width.after(1000, self.clock)  # .after(지연시간{ms}, 실행함수)

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller  # controller는 DispenserApp클래스를 가리킴

        self.clock_width = tk.Label(self, font=("Times", 24, "bold"), text="")
        self.clock()
        self.clock_width.pack(side="top", padx=10, pady=10)

        label = tk.Label(self, text="환영합니다", font=("Arial", 30))
        label.pack()
        label.place(x=300, y=200)

        start_btn = tk.Button(self, text="시작하기", overrelief="solid", width=10,
                              command=lambda: controller.show_frame("UserSetting"))
        start_btn.pack()


# 2. 사용자 초기 설정 프레임
class UserSetting(tk.Frame):

    def create_user(self):
        global user_cnt
        global new_user
        global pill_info
        pill_info = PillInfo(self.pill_name_input.get(), self.radio.get(), self.pill_cnt.get())
        user_cnt += 1
        new_user = UserInfo(user_cnt, self.name_input.get(), pill_info)
        self.controller.show_frame("PutPill")

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.name_label = tk.Label(self, text="사용자 이름: ")
        self.name_label.grid(row=0, column=0)
        self.name_input = tk.Entry(self, width=50)
        self.name_input.grid(row=0, column=1, columnspan=2)

        self.pill_label = tk.Label(self, text="복용할 약 이름: ")
        self.pill_label.grid(row=1, column=0)

        # 약 이름 입력받기
        self.pill_name_input = tk.Entry(self, width=50)
        self.pill_name_input.grid(row=1, column=1, columnspan=2)

        # 약통 선택
        bottle_label = tk.Label(self, text="약통 선택: ")
        bottle_label.grid(row=2, column=0)

        self.radio = tk.IntVar(self)
        self.one = tk.Radiobutton(self, text="1번", variable=self.radio, value=1)
        self.one.grid(row=2, column=1)
        self.two = tk.Radiobutton(self, text="2번", variable=self.radio, value=2)
        self.two.grid(row=2, column=2)

        # 약 복용량 입력
        self.pill_cnt_label = tk.Label(self, text="1회 복용량: ")
        self.pill_cnt_label.grid(row=3, column=0)
        self.pill_cnt = tk.Spinbox(self, from_=1, to=5)
        self.pill_cnt.grid(row=3, column=1, columnspan=2)

        # 이전 버튼
        prev_btn = tk.Button(self, text="이전으로",
                             command=lambda: controller.show_frame("StartPage"))
        prev_btn.grid(row=7, column=0)

        # 다음 버튼
        next_btn = tk.Button(self, text="다음으로", command=self.create_user)
        next_btn.grid(row=7, column=1)


# 3. 약을 넣어주세요
class PutPill(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label_text = "1번 통에 약을 넣고\n 확인 버튼을 눌러주세요!"
        self.label = tk.Label(self, text=label_text)
        self.label.pack()

        # 이전 버튼
        prev_btn = tk.Button(self, text="취소",
                             command=lambda: controller.show_frame("UserSetting"))
        prev_btn.pack(side="bottom", anchor="w")

        # 다음 버튼
        next_btn = tk.Button(self, text="확인",
                             command=lambda: controller.show_frame("AlarmSetting"))
        next_btn.pack(side="bottom", anchor="e")


# 4. 알람 설정 페이지
class AlarmSetting(tk.Frame):

    def setAlarm(self):
        new_alarm = AlarmInfo(self.alarm_hr.get(), self.alarm_mn.get(), self.sleep_hr.get(), self.sleep_mn.get())
        pill_info.setAlarm(new_alarm)
        AlarmCheck.getAlarmInfo(self.controller.frames["AlarmCheck"], pillInfo=pill_info)
        self.controller.show_frame("AlarmCheck")

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.label = tk.Label(self, text="알람 시간을 입력하세요.")
        self.label.grid(row=0, column=0, columnspan=4)

        # 알람 시간 입력
        self.alarm_hr = tk.Spinbox(self, from_=0, to=23, width=10, format="%02.0f")
        self.alarm_hr.grid(row=1, column=0)
        self.alarm_mn = tk.Spinbox(self, from_=0, to=59, width=10, format='%02.0f')
        self.alarm_mn.grid(row=1, column=1)

        self.alarm_time_label = tk.Label(self, text="알람 시간")
        self.alarm_time_label.grid(row=2, column=0, columnspan=2)

        self.sleep_hr = tk.Spinbox(self, from_=0, to=23, width=10, format="%02.0f")
        self.sleep_hr.grid(row=1, column=3)
        self.sleep_mn = tk.Spinbox(self, from_=0, to=59, width=10, format="%02.0f")
        self.sleep_mn.grid(row=1, column=4)

        self.sleep_time_label = tk.Label(self, text="취침 시간")
        self.sleep_time_label.grid(row=2, column=2, columnspan=2)

        # 다음 버튼
        next_btn = tk.Button(self, text="다음으로", command=self.setAlarm)
        next_btn.place(x=600, y=300)


# 5. 입력한 알람 설정 정보 확인 페이지
class AlarmCheck(tk.Frame):

    def getAlarmInfo(self, pillInfo):
        alarm_time = pillInfo.alarm.alarm_hr + ":" + pillInfo.alarm.alarm_mn
        sleep_time = pillInfo.alarm.sleep_hr + ":" + pillInfo.alarm.sleep_mn
        self.alarm_time.config(text=alarm_time)
        self.sleep_time.config(text=sleep_time)

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.label = tk.Label(self, text="입력한 정보를 확인하세요.")
        self.label.grid(row=0, column=0, columnspan=4)

        # 알람 시간 입력
        alarm_time = "00:00"
        sleep_time = "00:00"
        self.alarm_time = tk.Label(self, text=alarm_time)
        self.alarm_time.grid(row=1, column=0)
        self.alarm_time_label = tk.Label(self, text="알람 시간")
        self.alarm_time_label.grid(row=2, column=0)

        self.sleep_time = tk.Label(self, text=sleep_time)
        self.sleep_time.grid(row=1, column=1)
        self.sleep_time_label = tk.Label(self, text="취침 시간")
        self.sleep_time_label.grid(row=2, column=1)

        self.label2 = tk.Label(self, text="알람 설정 완료!\n복용 시간이 되면 알려드릴게요:)")
        self.label2.grid(row=3, column=0, columnspan=2)

        # 다음 버튼
        next_btn = tk.Button(self, text="확인",
                             command=lambda: controller.show_frame("StartPage"))
        next_btn.place(x=600, y=300)

# 6. 설정 완료 알림 페이지


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app = DispenserApp()
    app.mainloop()
