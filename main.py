import tkinter as tk
import time
from UserInfo import *

window = tk.Tk()
global now
global bottle_num
global user_cnt
user_cnt = 0

# # 시계
# def clock():
#     global now
#     now = time.strftime("%H:%M:%S")
#     StartPage.clock_width.config(text=now)
#     StartPage.clock_width.after(1000, clock) # .after(지연시간{ms}, 실행함수)


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
        for F in (StartPage, UserSetting, PutPill, AlarmSetting):
            page_name = F.__name__  # 각 class의 이름을 가져와서 저장
            frame = F(parent=container, controller=self)  # class의 _init_실행
            self.frames[page_name] = frame  # 각 class별 저장소에 각 class별 frame의 내용 저장

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")  # 각 프레임을 순서대로 화면에 출력

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        # "Show a frame for the given page name"
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

    def select_bottle(self):
        global bottle_num
        bottle_num = self.radio.get()
        print("선택된 약통: ", str(bottle_num))

    def create_user(self):
        global user_cnt
        pill_info = PillInfo(self.pill_name_input.get(), bottle_num, self.pill_cnt.get())
        user_cnt += 1
        UserInfo(user_cnt, self.name_input.get(), pill_info)
        self.controller.show_frame("PutPill")

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.name_label = tk.Label(self, text="사용자 이름: ")
        self.name_label.pack(pady=10)

        self.name_input = tk.Entry(self, width=50)
        self.name_input.pack(pady=10)

        self.pill_label = tk.Label(self, text="복용할 약 이름: ")
        self.pill_label.pack(pady=10)

        # 약 이름 입력받기
        self.pill_name_input = tk.Entry(self, width=50)
        self.pill_name_input.pack(pady=10)

        # 약통 선택
        bottle_label = tk.Label(self, text="약통 선택: ")
        bottle_label.pack()

        self.radio = tk.IntVar()
        self.one = tk.Radiobutton(self, text="1번", variable=self.radio, value=1, command=self.select_bottle)
        self.one.pack()
        self.two = tk.Radiobutton(self, text="2번", variable=self.radio, value=2, command=self.select_bottle)
        self.two.pack()

        # 약 복용량 입력
        self.pill_cnt_label = tk.Label(self, text="1회 복용량: ")
        self.pill_cnt_label.pack(pady=10)
        self.pill_cnt = tk.Spinbox(self, from_=1, to=5)
        self.pill_cnt.pack()

        # 이전 버튼
        prev_btn = tk.Button(self, text="이전으로",
                             command=lambda: controller.show_frame("StartPage"))
        prev_btn.pack(side="bottom")
        # 다음 버튼
        next_btn = tk.Button(self, text="다음으로", command=self.create_user)
        next_btn.pack(side="bottom")


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
        prev_btn.pack()

        # 다음 버튼
        next_btn = tk.Button(self, text="확인",
                             command=lambda: controller.show_frame("AlarmSetting"))
        next_btn.pack(side="bottom")


# 4. 알람 설정 페이지
class AlarmSetting(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.label = tk.Label(self, text="알람 시간을 입력하세요.")
        self.label.pack()

        # 다음 버튼
        next_btn = tk.Button(self, text="다음으로",
                             command=lambda: controller.show_frame("AlarmSetting"))
        next_btn.pack(side="bottom")


# 5. 입력한 알람 설정 정보 확인 페이지

# 6. 설정 완료 알림 페이지


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app = DispenserApp()
    app.mainloop()
