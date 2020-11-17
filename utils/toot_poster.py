from mastodon import Mastodon
import filetype
from .get_config import GetConfig

config = GetConfig()


def media_post(user_name, file):
  kind = filetype.guess(file)
  # print('File extension: %s' % kind.extension)
  # print('File MIME type: %s' % kind.mime)
  mastodon = Mastodon(access_token = config[user_name]['AccessToken'],api_base_url = config[user_name]['BaseUrl'])
  return mastodon.media_post(file, kind.mime)

def TootPoster(user_name, data):
  """
  :data object: Return from media_downloader
  :return void
  """
  media_ids_arr = []
  mastodon = Mastodon(access_token = config[user_name]['AccessToken'],api_base_url = config[user_name]['BaseUrl'])
  if data['video_count'] is not None:
    id=1
    if config[user_name]['IncludeVideo'] == 'false':
      media_ids_arr.append(media_post('temp/video%d.png' % id))
      # data['plain'] = data['plain'] + '\n'+config[user_name]['VideoSourcePrefix']+' ' + data['video_link']
    else:
      try:
        media_ids_arr.append(media_post('temp/video%d.mp4' % id))
      except Exception:
        media_ids_arr.append(media_post('temp/video%d.png' % id))
        # data['plain'] = data['plain'] + '\n'+config[user_name]['VideoSourcePrefix']+' ' + data['video_link']

  if data['image_count'] is not None:
    for id in range(1, min(data['image_count'], 5)):
      media_ids_arr.append(media_post('temp/img%d.png' % id))

  try:
    mastodon.status_post(status=data['plain'], media_ids=media_ids_arr, visibility=config[user_name]['TootVisibility'])
  except Exception:
    print(f'ERRO: failed[mastodon.status_post]')
    # for e in Exception:
    #   print(e)

if __name__ == '__main__':
  test_data = {'gif_count': 1, 'video_count': None, 'image_count': 3, 'plain': 'Tooting from python using `status_post` #mastodonpy !'}
  TootPoster(test_data)