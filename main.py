import tkinter as tk
import tkinter.ttk
import tkinter.messagebox

from UserInfo import *
from GPIO_setup import *

global now
global user_cnt
user_cnt = 1
global pill_info
global new_user
global user_time
info_list = []


# main window
class DispenserApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # self.attributes('-zoomed', True)  # 리눅스, 우분투 전체화면 설정
        self.attributes('-fullscreen', True)    # 윈도우 전체화면 설정
        self.title("Pill Dispenser")
        # self.geometry("750x500")
        self.resizable(True, True)

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


def getInfoTuple(user):
    user_info = (user.username, user.pillAlarm.pillname, user.pillAlarm.pill_cnt,
                 user.pillAlarm.alarm.alarm_time, user.pillAlarm.alarm.sleep_time,
                 user.pillAlarm.done)
    return user_info


# 1. 시계 프레임
class StartPage(tk.Frame):

    # 시계
    def clock(self):
        global now
        now = time.strftime("%H:%M:%S")
        self.clock_width.config(text=now)
        self.clock_width.after(1000, self.clock)  # .after(지연시간{ms}, 실행함수)
        # 0시 되면 초기화
        if now == "00:00:00":
            # 복용 여부가 No인 사용자 출력
            didnt = ""
            for i in range(len(user_list)):
                user = user_list[i]
                if user.pillAlarm.done == "No":
                    didnt = didnt + user.username + " "
                user.pillAlarm.done = "No"
                self.user_info_table.item(str(i), values=getInfoTuple(user))
            didnt = didnt + "\nDon't forget to take your medicine today! :)"
            self.msg_label.config(text=didnt)


        for i in range(len(user_list)):
            user = user_list[i]
            # 복용 여부가 No 일 때
            if user.pillAlarm.done == "No":
                if user.pillAlarm.alarm.alarm_time == now:
                    msg = "Now : " + now + "\n" + user.username + \
                          ", It's time to take your medicine:" + user.pillAlarm.pillname
                    alarm_play(user.id)
                    result = tk.messagebox.askyesno("Alarm", msg)
                    print(result)
                    if result:
                        # 약 복용
                        print("take medicine")
                        setting_prox(int(user.pillAlarm.pill_cnt))  # 근접 센서 활성화
                        user.pillAlarm.done = "Yes"
                        self.user_info_table.item(str(i), values=getInfoTuple(user))

                elif user.pillAlarm.alarm.sleep_time == now:
                    msg = "Now : " + now + "\n" + user.username + \
                          ", It's time to take your medicine:" + user.pillAlarm.pillname
                    alarm_play(user.id)
                    result = tk.messagebox.askyesno("Alarm", msg)
                    if result:
                        # 약 복용
                        print("Take a medicine before you sleep")
                        setting_prox(int(user.pillAlarm.pill_cnt))
                        user.pillAlarm.done = "Yes"
                        self.user_info_table.item(str(i), values=getInfoTuple(user))


    def update_user(self, user_info):
        self.user_info_table.insert('', 'end', text=str(user_cnt), values=user_info, iid=str(user_cnt - 1))

    def click_user(self, event):
        selectedUser = self.user_info_table.focus()
        getValue = self.user_info_table.item(selectedUser).get('values')
        msg = getValue[0] + ", it is " + getValue[3] + " when you take your medicine(" + getValue[1] + ")\n" \
              + "Do you want to take it right now and turn off the alarm? "
        result = tk.messagebox.askokcancel("Take your medicine - not alarm time", msg)
        if result:
            for i in range(len(user_list)):
                if user_list[i].username == getValue[0]:
                    setting_prox(int(user_list[i].pillAlarm.pill_cnt))  # 근접 센서 활성화
                    user_list[i].pillAlarm.done = "Yes"  # 복용 여부 True로 설정
                    # 표 업데이트
                    getValue[5] = "Yes"
                    self.user_info_table.item(selectedUser, values=getValue)
                    print("yes: activate prox")
        else:
            print("No: cancel")

    def direct_activate(self):
        msg = "Do you want to get your medicine once again?"
        result = tk.messagebox.askokcancel("Retry", msg)
        if result:
            print("yes: activate prox")
            setting_prox(1)  # 근접 센서 활성화
        else:
            print("No: cancel")

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.user_info_table = None
        self.controller = controller  # controller는 DispenserApp클래스를 가리킴

        self.clock_width = tk.Label(self, font=("Times", 24, "bold"), text="")
        self.clock()
        self.clock_width.grid(row=0, column=0, columnspan=2, sticky='n')

        self.user_info_table = tk.ttk.Treeview(self,
                                               columns=["User name", "Pill name", "Dosage", "Alarm", "Sleep", "Done"],
                                               displaycolumns=["User name", "Pill name", "Dosage", "Alarm", "Sleep",
                                                               "Done"])

        self.user_info_table.column("#0", width=50, anchor="center")
        self.user_info_table.heading("#0", text="Index")

        self.user_info_table.column("#1", width=100, anchor="center")
        self.user_info_table.heading("#1", text="User Name")

        self.user_info_table.column("#2", width=100, anchor="center")
        self.user_info_table.heading("#2", text="Pill Name")

        self.user_info_table.column("#3", width=50, anchor="center")
        self.user_info_table.heading("#3", text="Dose")

        self.user_info_table.column("#4", width=70, anchor="center")
        self.user_info_table.heading("#4", text="Alarm")

        self.user_info_table.column("#5", width=70, anchor="center")
        self.user_info_table.heading("#5", text="Sleep")

        self.user_info_table.column("#6", width=70, anchor="center")
        self.user_info_table.heading("#6", text="Done")

        # 표에 데이터 삽입
        for i in range(len(info_list)):
            self.user_info_table.insert('', 'end', text=str(i + 1), values=info_list[i], iid=str(i))

        self.user_info_table.bind('<ButtonRelease-1>', self.click_user)
        self.user_info_table.grid(row=1, column=0, columnspan=2, sticky='ew')

        self.msg_label = tk.Label(self, text="Have a nice day!\nDon't forget to take your medicine on time")
        self.msg_label.grid(row=2, column=0, columnspan=2, sticky='ew')

        activate_btn = tk.Button(self, text="One More", overrelief="solid", width=10,
                                 command=self.direct_activate)
        activate_btn.grid(row=3, column=0, sticky="sw")

        start_btn = tk.Button(self, text="Add User", overrelief="solid", width=10,
                              command=lambda: controller.show_frame("UserSetting"))
        start_btn.grid(row=3, column=1, sticky="se")


# 2. 사용자 초기 설정 프레임
class UserSetting(tk.Frame):

    def create_user(self):
        global user_cnt
        global new_user
        global pill_info
        pill_info = PillInfo(self.pill_name_input.get(), self.radio.get(), self.pill_cnt.get())
        user_cnt += 1
        new_user = UserInfo(user_cnt, self.name_input.get(), pill_info)
        label_text = "Put your medicine to " + str(new_user.pillAlarm.bottle_num) + "\n and press the button."
        self.controller.frames["PutPill"].label.config(text=label_text)
        self.controller.show_frame("PutPill")

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.name_label = tk.Label(self, text="user name: ")
        self.name_label.grid(row=0, column=0)
        self.name_input = tk.Entry(self, width=50)
        self.name_input.grid(row=0, column=1, columnspan=2, sticky='ew')

        self.pill_label = tk.Label(self, text="pill name: ")
        self.pill_label.grid(row=1, column=0)

        # 약 이름 입력받기
        self.pill_name_input = tk.Entry(self, width=50)
        self.pill_name_input.grid(row=1, column=1, columnspan=2)

        # 약통 선택
        bottle_label = tk.Label(self, text="select bottle: ")
        bottle_label.grid(row=2, column=0)

        self.radio = tk.IntVar(self)
        self.one = tk.Radiobutton(self, text="Bottle_1", variable=self.radio, value=1)
        self.one.grid(row=2, column=1)
        self.two = tk.Radiobutton(self, text="Bottle_2", variable=self.radio, value=2)
        self.two.grid(row=2, column=2)

        # 약 복용량 입력
        self.pill_cnt_label = tk.Label(self, text="dose: ")
        self.pill_cnt_label.grid(row=3, column=0)
        self.pill_cnt = tk.Spinbox(self, from_=1, to=5)
        self.pill_cnt.grid(row=3, column=1, columnspan=2)

        # 이전 버튼
        prev_btn = tk.Button(self, text="Prev",
                             command=lambda: controller.show_frame("StartPage"))
        prev_btn.grid(row=7, column=0)

        # 다음 버튼
        next_btn = tk.Button(self, text="Next", command=self.create_user)
        next_btn.grid(row=7, column=2)


# 3. 약을 넣어주세요
class PutPill(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label_text = "Put your medicine to bottle_1\n and press the button."
        self.label = tk.Label(self, text=label_text)
        self.label.pack()

        # 이전 버튼
        prev_btn = tk.Button(self, text="Cancel",
                             command=lambda: controller.show_frame("UserSetting"))
        prev_btn.pack(side="bottom", anchor="w")

        # 다음 버튼
        next_btn = tk.Button(self, text="OK",
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

        self.label = tk.Label(self, text="Enter your alarm time.")
        self.label.grid(row=0, column=0, columnspan=4)

        # 알람 시간 입력
        self.alarm_hr = tk.Spinbox(self, from_=0, to=23, width=10, format="%02.0f")
        self.alarm_hr.grid(row=1, column=0)
        self.alarm_mn = tk.Spinbox(self, from_=0, to=59, width=10, format='%02.0f')
        self.alarm_mn.grid(row=1, column=1)

        self.alarm_time_label = tk.Label(self, text="Alarm time")
        self.alarm_time_label.grid(row=2, column=0, columnspan=2)

        self.sleep_hr = tk.Spinbox(self, from_=0, to=23, width=10, format="%02.0f")
        self.sleep_hr.grid(row=1, column=3)
        self.sleep_mn = tk.Spinbox(self, from_=0, to=59, width=10, format="%02.0f")
        self.sleep_mn.grid(row=1, column=4)

        self.sleep_time_label = tk.Label(self, text="Sleep time")
        self.sleep_time_label.grid(row=2, column=2, columnspan=2)

        # 다음 버튼
        next_btn = tk.Button(self, text="Next", command=self.setAlarm)
        next_btn.place(x=600, y=300)


# 5. 입력한 알람 설정 정보 확인 페이지
class AlarmCheck(tk.Frame):

    def getAlarmInfo(self, pillInfo):
        self.alarm_time.config(text=pillInfo.alarm.alarm_time)
        self.sleep_time.config(text=pillInfo.alarm.sleep_time)

    # 사용자 보여주기
    def addUser(self):
        # 표에 삽입될 데이터
        new_user_info = getInfoTuple(new_user)
        info_list.append(new_user_info)
        user_list.append(new_user)
        StartPage.update_user(self.controller.frames["StartPage"], new_user_info)
        self.controller.show_frame("StartPage")

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.label = tk.Label(self, text="Check your information")
        self.label.grid(row=0, column=0, columnspan=4)

        # 알람 시간 입력
        alarm_time = "00:00"
        sleep_time = "00:00"
        self.alarm_time = tk.Label(self, text=alarm_time)
        self.alarm_time.grid(row=1, column=0)
        self.alarm_time_label = tk.Label(self, text="Alarm time")
        self.alarm_time_label.grid(row=2, column=0)

        self.sleep_time = tk.Label(self, text=sleep_time)
        self.sleep_time.grid(row=1, column=1)
        self.sleep_time_label = tk.Label(self, text="Sleep time")
        self.sleep_time_label.grid(row=2, column=1)

        self.label2 = tk.Label(self, text="Done!\nI'll let you know when it's time to take it:)")
        self.label2.grid(row=3, column=0, columnspan=2)

        # 다음 버튼
        next_btn = tk.Button(self, text="OK", command=self.addUser)
        next_btn.place(x=600, y=300)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # 초기 사용자 설정
    user1_alarm = AlarmInfo("23", "07", "23", "30")
    user1_pill_info = PillInfo("vitamin", 1, 1)
    user1_pill_info.setAlarm(user1_alarm)
    user1 = UserInfo(1, "yeonsu", user1_pill_info)
    user_list.append(user1)
    info_list.append(getInfoTuple(user1))

    #2
    user2_alarm = AlarmInfo("23", "40", "23", "50")
    user2_pill_info = PillInfo("omega-3", 1, 2)
    user2_pill_info.setAlarm(user2_alarm)
    user2 = UserInfo(1, "yewon", user2_pill_info)
    user_list.append(user2)
    info_list.append(getInfoTuple(user2))

    app = DispenserApp()

    app.mainloop()
