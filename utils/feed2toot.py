#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on May 29, 2020
Desc: feed to toot
Author: Mashiro 
URL: https://2heng.xin
License: MIT
"""
from itertools import filterfalse
from operator import truediv
from os import path, makedirs
import shutil
from .feed_decoder import TweetDecoder
from .media_downloader import MediaDownloader
from .toot_poster import TootPoster

def debugPrint(data):
  print()
  print()
  print(data)
  print()
  print()


def Feed2Toot(feed_data):
  if path.exists('db.txt'):
    historyList = [line.rstrip('\n') for line in open('db.txt')]
  else:
    historyList = []

  toot_finished = False

  for tweet in reversed(feed_data):
    if not path.exists('temp'):
      makedirs('temp')

    toot_able = True

    # 过滤 求转发 帮转 信息
    filterList = ["领养","转发","帮扩","求助","抽奖"]
    for filter in filterList:
      if filter in tweet['summary']:
        debugPrint("过滤 求转发 帮转 信息 忽略...")
        toot_able = False
        break

    if toot_able and tweet['id'] not in historyList:
      print('INFO: decode ' + tweet['id'])
      tweet_decoded = TweetDecoder(tweet)
      debugPrint(tweet_decoded)

      # 过滤 不符合推文
      # 过滤纯文本
      if not tweet_decoded['image']:
        # debugPrint("缺少img数据 忽略...")
        toot_able = False

      print('INFO: download ' + tweet['id'])
      if toot_able and not toot_finished:
        try:
          toot_content = MediaDownloader(tweet_decoded)
          print('INFO: download succeed ' + tweet['id'])
        except Exception:
          print('ERRO: download failed ' + tweet['id'])
          # for e in Exception:
          #   (e)
        print('INFO: post toot ' + tweet['id'])
        try:
          TootPoster(toot_content)
          print('INFO: post succeed ' + tweet['id'])
          toot_finished = True
        except Exception:
          print('ERRO: post failed ' + tweet['id'])

        historyList.append(tweet['id'])

    if path.exists('temp'):
      shutil.rmtree('temp')

    print('INFO: save to db ' + tweet['id'])
    with open('db.txt', 'w+') as db:
      for row in historyList:
        db.write(str(row) + '\n')
    
  return toot_finished

if __name__ == '__main__':
  test_feed = [{
    'title': "content",
    'summary': 'content <br><video src="https://video.twimg.com/ext_tw_video/1266540395799785472/pu/vid/544x960/DmN8_Scq1cZ7K3YR.mp4?tag=10" controls="controls" poster="https://pbs.twimg.com/ext_tw_video_thumb/1266540395799785472/pu/img/0vFhGUy_vv3j2hWE.jpg" style="width: 100%"></video> ',
    'id': 'https://twitter.com/zlj517/status/1266540485973180416',
    'link': 'https://twitter.com/zlj517/status/1266540485973180416',
  }]
  Feed2Toot(test_feed)