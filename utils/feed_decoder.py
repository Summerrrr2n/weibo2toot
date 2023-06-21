#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on May 29, 2020
Desc: Twitter HTML parser
Author: Mashiro 
URL: https://2heng.xin
License: MIT
"""
from bs4 import BeautifulSoup
from html import unescape
import re
from .get_config import GetConfig
# from get_config import GetConfig

config = GetConfig()


def debugPrint(data):
  print()
  print()
  print(data)
  print()
  print()



# def TweetDecoder(rss_data):
def TweetDecoder(rss_data):
  """
  :params object: Summary from FeedParaser
  :return object
  """
  # rss_data = {'title': '摸摸毛毛亲亲脑袋！[抱一抱] - 转发 @萨摩耶受益者联盟:&ensp;摸摸毛毛亲亲脑袋！ig：remy.samoyed | remy的妈咪真的好温柔哦！是相互治愈的存在！ 萨摩耶受益者...', 'summary': '摸摸毛毛亲亲脑袋！<span class="url-icon"><img alt="[抱一抱]" src="https://h5.sinaimg.cn/m/emoticon/icon/default/co_a1hug-f3910d0e88.png" style="width: 1em; height: 1em;" /></span><br /><blockquote> - 转发 <a href="https://weibo.com/7394892032" target="_blank">@萨摩耶受益者联盟</a>:\u2002摸摸毛毛亲亲脑袋！<br /><br />ig：remy.samoyed | remy的妈咪真的好温柔哦！是相互治愈的存在！ <a href="https://video.weibo.com/show?fid=1034:4684863085936657"><span class="url-icon"><img src="https://h5.sinaimg.cn/upload/2015/09/25/3/timeline_card_small_video_default.png" style="width: 1rem; height: 1rem;" /></span><span class="surl-text">萨摩耶受益者联盟的微博视频</span></a> </blockquote><br clear="both" /><div style="clear: both;"></div><video controls="controls" poster="https://wx3.sinaimg.cn/orj480/0084sde8gy1gure7e20d3j60k00baq4f02.jpg" style="width: 100%;"><source src="https://f.video.weibocdn.com/hrfYS4hVlx07Q48dZjxm010412001vQL0E010.mp4?label=mp4_hd&amp;template=640x360.25.0&amp;trans_finger=d8257cc71422c9ad30fe69ce9523c87b&amp;ori=0&amp;ps=1CwnkDw1GXwCQx&amp;Expires=1679474829&amp;ssig=kPl9nCoxhQ&amp;KID=unistore,video" /><source src="https://f.video.weibocdn.com/RH0pnL3Tlx07Q48e0fHq010412001Gin0E010.mp4?label=mp4_ld&amp;template=640x360.25.0&amp;trans_finger=6006a648d0db83b7d9951b3cee381a9c&amp;ori=0&amp;ps=1CwnkDw1GXwCQx&amp;Expires=1679474829&amp;ssig=kAoLhpvU0Y&amp;KID=unistore,video" /><p>视频无法显示，请前往<a href="https://video.weibo.com/show?fid=1034%3A4684863085936657&amp;luicode=10000011&amp;lfid=1076037394892032" rel="noopener noreferrer" target="_blank">微博视频</a>观看。</p></video>', 'id': 'https://weibo.com/7394892032/MymdNve8p', 'link': 'https://weibo.com/7394892032/MymdNve8p'}  # debugPrint(rss_data)
  soup = BeautifulSoup(rss_data['summary'], features='html.parser')

  data = {
      'video': [],
      'video_poster': [],
      'image': [],
      'plain': None
  }
  # debugPrint(soup)

  # 获取视频
  for link in soup.find_all('a'):
    # link.replace_with(' ' + link.get('href') + ' ')
    # print("aaaa",link)
    if (link.has_attr('data-url')):
      if ('://t.cn/' in link.get('data-url')):
        if ('微博视频' in link.getText()):
          link.replace_with(f'''[?bs4_replace_flag?] {config['MASTODON']['VideoSourcePrefix']} {link.getText()} {link.get('data-url')} [?bs4_replace_flag?]''')
        else:
          link.replace_with(f'''[?bs4_replace_flag?] {config['MASTODON']['ExternalLinkPrefix']} {link.getText()} {link.get('data-url')} [?bs4_replace_flag?]''')
      else:
        link.replace_with(f'''[?bs4_replace_flag?] {config['MASTODON']['ExternalLinkPrefix']} {link.getText()} {link.get('href')} [?bs4_replace_flag?]''')
    elif (link.getText()[-1] == '#'):
      link.replace_with(f'''[?bs4_replace_flag?] {link.getText()[:-1]} [?bs4_replace_flag?]''')
    else:
      link.replace_with('[?bs4_replace_flag?]'+link.getText()+'[?bs4_replace_flag?]')

  # 获取图片
  for span in soup.find_all('span'):
    if('url-icon' in span.get('class')):
      img = span.find('img')
      if not img:
        img.replace_with(img.get('alt'))
  # print('soup:', soup)

  source = soup.find('source')
  if source:
    # print('src:',source.get('src'))
    if source.get('src') and ('.mp4' in source.get('src')):
      # need to add a reffer i guess.
      data['video'].append(source.get('src'))

  video = soup.find('video')
  if video:
    # print('video:',video.get('poster'))
    if video.get('poster') and ('.jpg' in video.get('poster')):
      # need to add a reffer i guess.
      data['video_poster'].append(video.get('poster'))
      video.replace_with('')

  for image in soup.find_all('img'):
    # print(video.get('src'))

    #过滤表情

    if "emoticon/icon" in image.get('src'):
      continue


    if "appstyle/expression" in image.get('src'):
      continue

    data['image'].append(image.get('src'))
    image.replace_with('')

  for br in soup.find_all('br'):
    br.replace_with('<|n>')

  for span in soup.find_all('span'):
    span.replace_with('')
    # span.replace_with(span.text)

  for div in soup.find_all('div'):
    div.replace_with('')

  for blockquote in soup.find_all('blockquote'):
    blockquote.unwrap()
  
  # print(soup.prettify())
  # print(str(data))
  # plain_content = unescape(soup.prettify())
  # plain_content = plain_content.split("<")[0]
  # plain_content = plain_content.replace('  ', ' ')
  # plain_content = plain_content.replace('\n[?bs4_replace_flag?]',' ').replace('[?bs4_replace_flag?]\n',' ').replace('[?bs4_replace_flag?]','').replace('\n- ','\n\- ').replace('<|n>','\n')
  # plain_content = re.sub(r'(#[^#]+)#', lambda m : m.group(1)+' ', plain_content)
  
  # print(type(rss_data['summary']))
  plain_content = rss_data['summary'].split('<')[0]
  data['plain'] = plain_content + '\n'+config['MASTODON']['SourcePrefix']+' ' + rss_data['link'] + '\n'+ 'Source:' +' ' + '/'.join(rss_data['id'].split('/')[0:-1])
  # debugPrint(data)
  return data 

if __name__ == '__main__':
  test_video = """
Xin Chun Kuai Le to my dear friends in China! Follow <a href="https://weibo.com/n/GranityStudios">@GranityStudios</a> to discover all the New Year gifts from me. <a data-url="http://t.cn/A6P4vrdP" href="https://video.weibo.com/show?fid=1034:4464353139949610" data-hide>KobeBryant的微博视频</a> <br><video src="http://f.video.weibocdn.com/0007wH7vlx07ApA2w7Fu010412004Apj0E010.mp4?label=mp4_hd&template=852x480.25.0&trans_finger=62b30a3f061b162e421008955c73f536&ori=0&ps=1CwnkDw1GXwCQx&Expires=1596472597&ssig=jdYuH97zC0&KID=unistore,video" controls="controls" poster="https://wx4.sinaimg.cn/orj480/c28dca85ly1gb7wzu6nolj21hc0u0gp6.jpg" style="width: 100%"></video>
"""
  print(TweetDecoder(test_video))