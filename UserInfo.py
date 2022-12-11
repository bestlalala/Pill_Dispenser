global user_list
user_list = list()
class UserInfo:
    def __init__(self, id, username, PillInfo):
        self.id = id
        self.username = username
        self.pillAlarm = PillInfo
        print("user info 생성: ", self.username, self.pillAlarm)
        global user_list
        user_list.append(self)
        for user in user_list:
            print(user.username)


class PillInfo:
    def __init__(self, pillname, bottle_num, pill_cnt):
        self.alarm = None
        self.pillname = pillname
        self.bottle_num = bottle_num
        self.pill_cnt = pill_cnt
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
        print("알람 시간: ", self.alarm.alarm_hr+":"+self.alarm.alarm_mn)
        print("취침 시간: ", self.alarm.sleep_hr+":"+self.alarm.sleep_hr)


class AlarmInfo:
    def __init__(self, alarm_hr, alarm_mn, sleep_hr, sleep_mn):
        self.alarm_hr = alarm_hr
        self.alarm_mn = alarm_mn
        self.sleep_hr = sleep_hr
        self.sleep_mn = sleep_mn
        print("----알람 생성 완료----")
        print("알람 시간: ", self.alarm_hr+":"+self.alarm_mn)
        print("취침 시간: ", self.sleep_hr+":"+self.sleep_mn)