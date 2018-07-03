import urllib3
import certifi
import json
import pandas as pd
from googletrans import Translator
import emoji
import webbrowser

base_url = 'https://www.googleapis.com/youtube/v3/search?'
api_key = 'AIzaSyDlITOYKP8ABriX7UZisXTF9DDtTfma480'

#change 'Grab' to what you want to search for, and change 'maxResults=10' to liking

remainder = 'part=snippet&order=date&maxResults=50&' + 'q=' + 'Grab+mod' + '&key=' + api_key
url = base_url + remainder

video_id = []
title = []
published_at = []


next_page_tokens = ['CDIQAA', 'CGQQAA', 'CJYBEAA', 'CMgBEAA', 'CPoBEAA', 'CKwCEAA', 'CN4CEAA', 'CJADEAA', 'CMIDEAA', 'CPQDEAA']

next_url = base_url + 'pageToken=' + str(next_page_tokens[0]) + '&' + remainder
http = urllib3.PoolManager(cert_reqs = 'CERT_REQUIRED', ca_certs=certifi.where())
r = http.request('GET', url)
response = r.data
data = json.loads(response)
items = data['items']

for item in items:
    if item['id']['kind'] == 'youtube#video':
        videoid = item['id']['videoId']
        video_id.append(videoid)
        snippet = item['snippet']
        title.append(snippet['title'])
        published_at.append(snippet['publishedAt'])

#formatting data and translating

df = pd.DataFrame(published_at, columns = ['published_at'])
df['video_id']=video_id
df['title']=title

translator = Translator()
translated = []
for row in df['title']:
    try:
        translated.append(translator.translate(row).text)
    except ValueError:
        translated.append('translate manually')

df['title_translated']=translated

relevance = []
for id in df['video_id']:
    webbrowser.open_new_tab('https://www.youtube.com/watch?v=' + str(id))
    value = input('relevance ')
    relevance.append(value)

df['relevance']=relevance

df.to_excel('/Users/claudia.seow/Desktop/YouTube Scraper/videos_mod.xlsx', index=False)