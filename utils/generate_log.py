
import time
import datetime
import os
from os import path
import random
from .get_config import GetConfig

date = time.strftime("%Y-%m-%d", time.localtime())
cur_time = time.strftime("%H:%M:%S", time.localtime())

summary = ["今天工作进行得很顺利，大家都很喜欢我的嘟嘟！", "总之今天过得超棒，我发的每一条嘟嘟都收到了好多人的喜欢！", "今天超级开心呀！每隔一个小时我都在Mastodon上发了超级可爱的狗狗照片或者视频！", "总之今天我超棒，我发的嘟嘟收到了好多人的喜欢！",
           "今天我也在Mastodon上发了好多可爱的狗狗照片！", "总之今天发嘟嘟的事情进行得很顺利，大家都超级喜欢我的嘟嘟！", "总的来说，今天我的嘟嘟发送得非常顺利，大家很喜欢！", "总的来说，今天我的嘟嘟发送得非常顺利，大家都很喜欢！"]
firstRecordInTheDay = ["成功发送啦！", "这次发送很顺利的哦！", "耶，这次发送非常成功！", "这次发送很顺利哦！", "成功啦，大家都夸我发的狗狗好可爱！",
                       "发送顺利，收到了好多喜欢！", "成功啦，有人转发了我的嘟嘟！", "哇，这次发送超级顺利！", "嘿嘿，这次发送很棒！", "成功啦，我的嘟嘟好像很受欢迎！", "太棒了，这次发送很顺利！", "成功啦，收获了几个喜欢！", "成功发送了一条可爱小狗的动态！"]
otherRecordInTheDay = ["这次发送也很顺利哦！", "这次发送也很顺利的哦！", "耶，这次发送也非常成功！"]
failedRecord = ["啊呀，这次发送没有成功。", "唉呀，这次发送失败了。",
                "嘟嘟没有发出去！", "糟糕，这次发送失败了。", "啊，出了点问题，发送失败了。"]

config = GetConfig()

def getYesterday():
    today = datetime.date.today()
    oneday = datetime.timedelta(days=1)
    yesterday = today-oneday
    return yesterday


def randomWoof(text, failed=False):
    woof = ""
    if random.randint(1, 100) > 50:
        woof = '汪' * random.randint(1, 3) + "！"
    else:
        woof = '嗷' + "呜" * random.randint(1, 3) + "~！"
    if failed:
        woof = '呜' * random.randint(1, 3) + "~"


    if random.randint(1, 100) > 50:
        return text + woof
    else:
        return woof + text

def GenerateSummary(isSuccess):
    if isSuccess:
        return "\n\n" + config['MASTODON']['SourcePrefix']+ " " + randomWoof(random.choice(summary)) + "大家晚安！明天见！"
    else:
        return "\n\n" + config['MASTODON']['SourcePrefix']+ " "  + randomWoof("今天有点小失误，大家晚安！明天见！")
    
def writeSingleRecord():
    record = ""
    if cur_time.split(':')[0] == '00':
        record = random.choice(firstRecordInTheDay)
    else:
        record = random.choice(firstRecordInTheDay + otherRecordInTheDay)
    return randomWoof(record)


def initialLog():
    # 删除昨天的log
    yesterday = getYesterday()
    if path.exists("email_%s.txt" % yesterday):
        os.remove("email_%s.txt" % yesterday)
    if not path.exists("email_%s.txt" % date):
        create_log = open("email_%s.txt" % date, 'w')
        create_log.close()

    # 写今日log
    # 标题
    log_date = open("email_%s.txt" % date, 'r+')
    first_line = log_date.readline().rstrip()
    if first_line != date:
        log_date.write(date + '\n')
    log_date.close()


def GenerateFailedLog():
    initialLog()
    # 内容
    log_content = open("email_%s.txt" % date, 'a')
    log_content.write(cur_time+": " + randomWoof(random.choice(failedRecord), True) + '\n')
    log_content.close()


def GenerateSuccessLog():
    initialLog()

    # 内容
    log_content = open("email_%s.txt" % date, 'a')
    log_content.write(cur_time+": " + writeSingleRecord() + '\n')
    log_content.close()


def GetGitAutoPullLog():
    log = open("gitlog.txt", 'r+')
    return '\nGit Auto Pull Log:\n'+ log.read()

def GetTodayLog():
    if cur_time.split(':')[0] != '23':
        return False
    else:
        log = open("email_%s.txt" % date, 'r+')
        return log.read()


if __name__ == '__main__':
    print(GenerateSuccessLog())
    print(GenerateFailedLog())
    # GenerateFailedLog()
