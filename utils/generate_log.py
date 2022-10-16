
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
    if not path.exists("email_%s.txt" % date):
        create_log = open("email_%s.txt" % date,'w')
        create_log.close()

    # 写今日log
    # 标题
    log_date = open("email_%s.txt" % date, 'r+')
    first_line = log_date.readline().rstrip()
    if first_line != date:
        log_date.write(date + '\n')
    log_date.close()

    #内容
    log_content = open("email_%s.txt" % date, 'a')
    log_content.write(cur_time+": "+text+'\n')
    log_content.close()


def GetTodayLog():
    if cur_time.split(':')[0] != '23':
        return False
    else:
        log = open("email_%s.txt" % date, 'r+')
        return log.read()


if __name__ == '__main__':
    text = 'aaa'
    GenerateLog(text)
