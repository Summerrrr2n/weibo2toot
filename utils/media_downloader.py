#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on May 29, 2020
Desc: Media file downloader
Author: Mashiro 
URL: https://2heng.xin
License: MIT
"""
import urllib.request
# import ffmpy
from .get_config import GetConfig
# from get_config import GetConfig
config = GetConfig()

def MediaDownloader(data):
  """
  :param object: Data return from TweetDecoder
  :return {'gif_count': (max+1)gif_id, 'video_count': video_id, 'image_count': img_id, 'plain': str}
  """
  # set header
  opener = urllib.request.build_opener()
  opener.addheaders = []
  opener.addheaders.append(('User-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'))
  opener.addheaders.append(('Referer', 'https://weibo.com/'))
  urllib.request.install_opener(opener)

  res = {'video_count': None, 'image_count': None, 'plain': None, 'video_link': None}

  if data['image']:
    img_id = 1
    for url in data['image']:
      if (img_id <= 4):
        try:
          urllib.request.urlretrieve(url, 'temp/img'+str(img_id)+'.png')
          img_id = img_id+1
        except Exception:
          print(f'ERRO: failed[img]: {url}')
          # for e in Exception:
          #   print(e)

    res['image_count']=img_id

  if data['video']:
    video_id = 1
    for url in data['video']:
      if (video_id <= 1):
        try:
          if config['MASTODON']['IncludeVideo'] != 'false':
            urllib.request.urlretrieve(url, 'temp/video'+str(video_id)+'.mp4')

          urllib.request.urlretrieve(data['video_poster'][video_id-1], 'temp/video'+str(video_id)+'.png')
          res['video_link']=url
          video_id = video_id+1
        except Exception:
          print(f'ERRO: failed[vid]: {url}')
          # for e in Exception:
          #   print(e)

    res['video_count']=video_id
  
  res['plain']=data['plain']
  # print(res)

  return res

if __name__ == '__main__':
  test_data = {'video': ['https://f.video.weibocdn.com/hrfYS4hVlx07Q48dZjxm010412001vQL0E010.mp4?label=mp4_hd&template=640x360.25.0&trans_finger=d8257cc71422c9ad30fe69ce9523c87b&ori=0&ps=1CwnkDw1GXwCQx&Expires=1679474829&ssig=kPl9nCoxhQ&KID=unistore,video'], 'video_poster': ['https://wx3.sinaimg.cn/orj480/0084sde8gy1gure7e20d3j60k00baq4f02.jpg'], 'image': [], 'plain': '摸摸毛毛亲亲脑袋！\n:dance_cool_doge: https://weibo.com/7394892032/MymdNve8p'}
  MediaDownloader(test_data)