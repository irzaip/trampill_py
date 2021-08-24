import yaml
import urllib.parse as urlparse
from urllib.parse import parse_qs


#  Ini modul koneksi ke Youtube data API v3
#  harus ada api_key
#
#   Contoh file api.yaml
#   api_key: 'blabablablabla'
#   api key youtube data v3 - only for read data.


#f = open('api.yaml','rt')
#config = yaml.load(f, Loader=yaml.FullLoader)
#f.close()

#api_key = config['api_key']
#print(api_key)

from googleapiclient.discovery import build


def _ytb_video(api_key, id=""):

    yt = build('youtube', 'v3', developerKey=api_key)

    client = yt.videos().list(part='snippet,contentDetails,statistics',id=id)
    response = client.execute()
    vid_url = 'https://youtube.com/watch?v='+str(id)
    vid_detail = []
    vid_detail.append(response['items'][0]['snippet']['title'])
    vid_detail.append(vid_url)
    try:
        vid_detail.append(response['items'][0]['snippet']['thumbnails']['standard']['url'])
    except: pass
    return vid_detail

def _ytb_playlist(api_key, id=""):

    yt = build('youtube', 'v3', developerKey=api_key)

    client = yt.playlistItems().list(
        part="contentDetails",
        maxResults = 150,
        playlistId=id
    )
    response = client.execute()
    response = response['items']
    vid_ids = []
    for i in response:
        vid_ids.append(i['contentDetails']['videoId'])
    return vid_ids

def get_content(url, api_key):

    yt = build('youtube', 'v3', developerKey=api_key)

    parsed = urlparse.urlparse(url)
    playlist = parse_qs(parsed.query)['list'][0]

    myvid = _ytb_playlist(api_key, playlist )
    videos = []
    for vid in myvid:
        try:
            videos.append(_ytb_video(api_key, vid))
        except:
            pass
    print(videos)
    return videos


if __name__ == '__main__':
    #myvid = _ytb_playlist('PLxBhf17jrfxEnd8SZOxNyEc6cgZZZWziH')
    #print(myvid)

    api_key= input("Masukkan api key:")
    url = input("Masukkan url yang akan di proses")
    result = get_content(url, api_key)
    print(result)


