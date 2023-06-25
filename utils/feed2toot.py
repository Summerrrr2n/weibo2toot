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



def getLog():
  # create or read db.txt/filter_log.txt
  if path.exists('db.txt'):
    historyList = [line.rstrip('\n') for line in open('db.txt')]
  else:
    historyList = []
  if path.exists('filter_log.txt'):
    filterLogList = [line.rstrip('\n') for line in open('filter_log.txt', encoding='utf8')]
  else:
    filterLogList = []
  return historyList, filterLogList

def updateLog(id, historyList, filterLogList):
  # log
  print('INFO: save to db ' + id)
  with open('db.txt', 'w+') as db:
    for row in historyList:
      db.write(str(row) + '\n')
  with open('filter_log.txt', 'w+', encoding='utf8') as filter_log:
    for row in filterLogList:
      filter_log.write(str(row) + '\n')


def adChecker(tweet, historyList, filterLogList):
  # ad filtered
  filterList = ["https://weibo.com/p/","taobao","shop.sc.weibo.com","旗舰店","领券","券后","福利","到货","抽奖","快递","售价","团购","价格","秒杀","补贴","购买","狂欢","好物","6.18","双11","双十一","大促","限时","速抢","拼团","特价","预售","爆款","超值","实惠","新品","活动价","天猫","京东","tao宝","淘宝","11.11","购物节","粉丝群"]
  toot_able = True
  for filter in filterList:
    if filter in tweet['summary']:
      filterLogList.append(filter + ' ad :' + tweet['id'])
      historyList.append(tweet['id'])
      print('INFO: ad ' , tweet)
      toot_able = False
      break
  return toot_able


def Feed2Toot(feed_data):
  historyList, filterLogList = getLog()
  toot_finished = False

  # sort by latest
  for tweet in reversed(feed_data):
    if not path.exists('temp'):
      makedirs('temp')

    # check if alreay filted or posted
    if tweet['id'] in historyList:
      continue
    
    # ad filtered
    toot_able = adChecker(tweet, historyList, filterLogList)

    # if not already filtered or posted, then decode
    if toot_able:
      print('INFO: decode ' + tweet['id'])
      tweet_decoded = TweetDecoder(tweet)

      # no media filter
      if not tweet_decoded['image'] and not tweet_decoded['video']:
        toot_able = False
        filterLogList.append('no media :' + tweet['id'])
        historyList.append(tweet['id'])

      print('INFO: download ' + tweet['id'])
      if toot_able and not toot_finished:
        try:
          toot_content = MediaDownloader(tweet_decoded)
          print('INFO: download succeed ' + tweet['id'])
        except Exception as err:
          print(f"Unexpected {err=}, {type(err)=}")
          print('ERRO: download failed ' + tweet['id'])

        print('INFO: post toot ' + tweet['id'])
        try:
          toot_finished = TootPoster(toot_content)
        except Exception as err:
          print(f"Unexpected {err=}, {type(err)=}")
          print('ERRO: post failed ' + tweet['id'])

    if path.exists('temp'):
      shutil.rmtree('temp')

    # check if toot alreay finished
    if toot_finished:
      print('INFO: post succeed ' + tweet['id'])
      historyList.append(tweet['id'])
      
    # log
    updateLog(tweet['id'], historyList, filterLogList)

    # exit if toot finished
    if toot_finished:
      break
    

  return toot_finished

if __name__ == '__main__':
  test_feed = [{'title': '摸摸毛毛亲亲脑袋！[抱一抱] - @萨摩耶受益者联盟:&ensp;摸摸毛毛亲亲脑袋！ig：remy.samoyed | remy的妈咪真的好温柔哦！是相互治愈的存在！ 萨摩耶受益者...', 'summary': '摸摸毛毛亲亲脑袋！<span class="url-icon"><img alt="[抱一抱]" src="https://h5.sinaimg.cn/m/emoticon/icon/default/co_a1hug-f3910d0e88.png" style="width: 1em; height: 1em;" /></span><br /><blockquote> - <a href="https://weibo.com/7394892032" target="_blank">@萨摩耶受益者联盟</a>:\u2002摸摸毛毛亲亲脑袋！<br /><br />ig：remy.samoyed | remy的妈咪真的好温柔哦！是相互治愈的存在！ <a href="https://video.weibo.com/show?fid=1034:4684863085936657"><span class="url-icon"><img src="https://h5.sinaimg.cn/upload/2015/09/25/3/timeline_card_small_video_default.png" style="width: 1rem; height: 1rem;" /></span><span class="surl-text">萨摩耶受益者联盟的微博视频</span></a> </blockquote><br clear="both" /><div style="clear: both;"></div><video controls="controls" poster="https://wx3.sinaimg.cn/orj480/0084sde8gy1gure7e20d3j60k00baq4f02.jpg" style="width: 100%;"><source src="https://f.video.weibocdn.com/hrfYS4hVlx07Q48dZjxm010412001vQL0E010.mp4?label=mp4_hd&amp;template=640x360.25.0&amp;trans_finger=d8257cc71422c9ad30fe69ce9523c87b&amp;ori=0&amp;ps=1CwnkDw1GXwCQx&amp;Expires=1679474829&amp;ssig=kPl9nCoxhQ&amp;KID=unistore,video" /><source src="https://f.video.weibocdn.com/RH0pnL3Tlx07Q48e0fHq010412001Gin0E010.mp4?label=mp4_ld&amp;template=640x360.25.0&amp;trans_finger=6006a648d0db83b7d9951b3cee381a9c&amp;ori=0&amp;ps=1CwnkDw1GXwCQx&amp;Expires=1679474829&amp;ssig=kAoLhpvU0Y&amp;KID=unistore,video" /><p>视频无法显示，请前往<a href="https://video.weibo.com/show?fid=1034%3A4684863085936657&amp;luicode=10000011&amp;lfid=1076037394892032" rel="noopener noreferrer" target="_blank">微博视频</a>观看。</p></video>', 'id': 'https://weibo.com/7394892032/MymdNve8p', 'link': 'https://weibo.com/7394892032/MymdNve8p'}]
  Feed2Toot(test_feed)
