#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on May 29, 2020
Desc: Twitter feed to toot (based on RSSHub's feed)
Author: Mashiro 
URL: https://2heng.xin
License: MIT
"""
import random
from utils.feed_parser import FeedParaser
from utils.feed2toot import Feed2Toot
from utils.get_config import GetConfig
from utils.send_email import SendEmail
from utils.generate_log import GenerateLog, GetTodayLog
import os

config = GetConfig()

if __name__ == '__main__':
    if config['PROXY']['ProxyOn'] == 'true':
        os.environ['HTTP_PROXY'] = config['PROXY']['HttpProxy']
        os.environ['HTTPS_PROXY'] = config['PROXY']['HttpsProxy']
    runSuccess = False
    # 随机选择一个rss源
    while not runSuccess:
        RSS_dict = []
        tryRssTime = 0
        while len(RSS_dict) == 0 and tryRssTime < 10:
            # 随机选择一个rss源直到解析成功,最大尝试次数10
            RSSList = eval(config['WEIBO']['RSSList'])
            RSSAddress = config['WEIBO']['WeiboRssAPI'] + \
                str(random.sample(RSSList, 1)[0])
            RSS_dict = FeedParaser(RSSAddress)
            tryRssTime += 1
        if (len(RSS_dict) != 0):
            runSuccess = Feed2Toot(RSS_dict)

    result = 'Success.' if runSuccess else 'Not Success.' 
    log_text = 'run over, this time is ' + result
    GenerateLog(log_text)

    # 发送今日邮件
    contents = GetTodayLog()
    if contents:
        fromAD = config['EMAIL']['From']
        toAD = config['EMAIL']['To']
        passport = config['EMAIL']['Password']
        host = config['EMAIL']['Host']
        subject = config['EMAIL']['Subject']
        SendEmail(fromAD, passport, toAD, host, subject, contents)
