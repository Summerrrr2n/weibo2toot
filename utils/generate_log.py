
import time
import datetime
import os
from os import path



date = time.strftime("%Y-%m-%d", time.localtime())
cur_time = time.strftime("%H:%M:%S", time.localtime())

def getYesterday():
    today = datetime.date.today()
    oneday = datetime.timedelta(days=1)
    yesterday = today-oneday
    return yesterday


def GenerateLog(text):
    # 删除昨天的log
    yesterday = getYesterday()
    if path.exists("email_%s.txt" % yesterday):
        os.remove("email_%s.txt" % yesterday)

    # 写今日log
    log = open("email_%s.txt" % date, 'w+')
    first_line = log.readline().rstrip()
    if first_line != date:
        log.write(date + '\n')
    log.write(cur_time+": "+text)


def GetTodayLog():
    if cur_time.split(':')[0] != '23':
        return False
    else:
        log = open("email_%s.txt" % date, 'r+')
        return log.read()


if __name__ == '__main__':
    text = 'aaa'
    GenerateLog(text)
