class UserInfo:
    def __init__(self, id, username, PillInfo):
        self.id = id
        self.username = username
        self.pillAlarm = PillInfo
        print("user info 생성: ", self.username, self.pillAlarm)


class PillInfo:
    def __init__(self, pillname, bottle_num, pill_cnt):
        self.alarm = None
        self.pillname = pillname
        self.bottle_num = bottle_num
        self.pill_cnt = pill_cnt
        print("pill info 생성: ", self.pillname, self.bottle_num, pill_cnt)

    def setAlarm(self, alarm):
        self.alarm = alarm
        print("alarm 설정: ", self.alarm)
