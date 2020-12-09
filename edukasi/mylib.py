
# my private library
import urllib.parse as urlparse

def get_yt_v(url):
    url_data = urlparse.urlparse(url)
    query = urlparse.parse_qs(url_data.query)
    video = query["v"][0]
    return video

