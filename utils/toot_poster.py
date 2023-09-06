from mastodon import Mastodon
import filetype
from .get_config import GetConfig
# from get_config import GetConfig

config = GetConfig()

mastodon = Mastodon(
  access_token = config['MASTODON']['AccessToken'],
  api_base_url = config['MASTODON']['BaseUrl']
)

def media_post(file):
  kind = filetype.guess(file)
  return mastodon.media_post(file, kind)

def TootPoster(data):
  """
  :data object: Return from media_downloader
  :return void
  """
  media_ids_arr = []
  toot_success = False

  if data['video_count'] is not None:
    id=1
    if config['MASTODON']['IncludeVideo'] == 'false':
      media_ids_arr.append(media_post('temp/video%d.png' % id))
      # data['plain'] = data['plain'] + '\n'+config['MASTODON']['VideoSourcePrefix']+' ' + data['video_link']
    else:
      try:
        media_ids_arr.append(mastodon.media_post('temp/video%d.mp4' % id, filetype.guess('temp/video1.mp4'),synchronous=True))
      except Exception as err:
        print(f"INFO: append video failed for unexpected {err=}, {type(err)=}")
        toot_success = False

        # media_ids_arr.append(media_post('temp/video%d.png' % id))
        # data['plain'] = data['plain'] + '\n'+config['MASTODON']['VideoSourcePrefix']+' ' + data['video_link']

  elif data['image_count'] is not None:
    for id in range(1, min(data['image_count'], 5)):
      media_ids_arr.append(media_post('temp/img%d.png' % id))
  
  if len(media_ids_arr) >= 1 :
    try:
      mastodon.status_post(status=data['plain'],
                            media_ids=media_ids_arr, visibility=config['MASTODON']['TootVisibility']
                            )
      toot_success = True
    except Exception as err:
      print(f'ERRO: failed[mastodon.status_post] for unexpected {err=}, {type(err)=}')
      toot_success = False

  return toot_success

if __name__ == '__main__':
  test_data = {'gif_count': 1, 'video_count': None, 'image_count': 3, 'plain': 'Tooting from python using `status_post` #mastodonpy !'}
  TootPoster(test_data)