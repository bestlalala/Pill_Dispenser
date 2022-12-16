global user_list
user_list = list()


class UserInfo:

    def __init__(self, id, username, PillInfo):
        self.id = id
        self.username = username
        self.pillAlarm = PillInfo
        print("user info 생성: ", self.username, self.pillAlarm)

    # def appendList(self):
    #     global user_list
    #     user_list.append(self)
    #     print("user_list: ", user_list)


class PillInfo:
    def __init__(self, pillname, bottle_num, pill_cnt):
        self.alarm = None
        self.pillname = pillname
        self.bottle_num = bottle_num
        self.pill_cnt = pill_cnt
        self.done = False   # 복용 여부
        print("pill info 생성: ", self.pillname, self.bottle_num, pill_cnt)

    def setAlarm(self, alarm_info):
        self.alarm = alarm_info
        print("alarm 설정: ", self.alarm)
        for user in user_list:
            print(user.username)
            user.pillAlarm.showAlarm()

    def showAlarm(self):
        print("약 이름: ", self.pillname)
        print("약 개수: ", self.pill_cnt)
        print("알람 시간: ", self.alarm.alarm_time)
        print("취침 시간: ", self.alarm.sleep_time)


class AlarmInfo:
    def __init__(self, alarm_hr, alarm_mn, sleep_hr, sleep_mn):
        self.alarm_time = alarm_hr + ":" + alarm_mn + ":00"
        self.sleep_time = sleep_hr + ":" + sleep_mn + ":00"
        print("----알람 생성 완료----")
        print("알람 시간: ", self.alarm_time)
        print("취침 시간: ", self.sleep_time)
