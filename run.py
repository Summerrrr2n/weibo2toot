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
from utils.generate_log import GenerateSuccessLog, GetTodayLog, GenerateFailedLog, GetGitAutoPullLog, GenerateSummary, CronDeleteLog
from utils.toot_poster import TootPosterLog
import os

config = GetConfig()

if __name__ == '__main__':
    if config['PROXY']['ProxyOn'] == 'true':
        os.environ['HTTP_PROXY'] = config['PROXY']['HttpProxy']
        os.environ['HTTPS_PROXY'] = config['PROXY']['HttpsProxy']
    runSuccess = False
    # 随机选择一个rss源
    tryTime = 0
    maxRetry = 10
    while not runSuccess and tryTime < maxRetry:
        RSS_dict = []
        while len(RSS_dict) == 0 and tryTime < maxRetry:
            # 随机选择一个rss源直到解析成功,最大尝试次数10
            RSSList = eval(config['WEIBO']['RSSList'])
            RSSAddress = config['WEIBO']['WeiboRssAPI'] + \
                str(random.sample(RSSList, 1)[0])
            RSS_dict = FeedParaser(RSSAddress)
            tryTime += 1
        if (len(RSS_dict) != 0):
            runSuccess = Feed2Toot(RSS_dict)

    if runSuccess:
        GenerateSuccessLog()
    else:
        GenerateFailedLog()

    # 发送今日邮件
    contents = GetTodayLog()
    summary = GenerateSummary(runSuccess)
    if contents:
        fromAD = config['EMAIL']['From']
        toAD = config['EMAIL']['To']
        passport = config['EMAIL']['Password']
        host = config['EMAIL']['Host']
        subject = config['EMAIL']['Subject']
        TootPosterLog("#puppyBot工作日志 " + contents + summary)
        SendEmail(fromAD, passport, toAD, host, subject,
                  contents + GetGitAutoPullLog())
        
    CronDeleteLog()
