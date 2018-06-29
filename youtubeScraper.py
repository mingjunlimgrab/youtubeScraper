# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import urllib3
import certifi
import json
import pandas as pd
import numpy as np
#from googletrans import Translator
#import emoji
#import textblob


# Load existing DataFrame (named test.csv). If unable to find, start from scratch.
try:
    old_df = pd.read_csv('test.csv')
    video_id = (old_df['video_id']).tolist()
    title = (old_df['title']).tolist()
    description = (old_df['description']).tolist()
    published_at = (old_df['published_at']).tolist()
    seen = set(video_id)
except:
    seen = {}
    video_id = []
    title = []
    description = []
    published_at = []
    print('no file found')
    
try:
    tokn = open("tokensSeen.json", "r")
    tokensSeen = json.loads(tokn)
except:
    print('tokens seen not found')
    tokensSeen = []

# Modifyable search parameters (CHANGE ME)
search_params = 'Grab' # Params seperated by + (eg. ‘Grab+fake+app’ or ‘Grab+tutorial’)
num_pages = 10
results_per_page = 50
# Modifyable search parameters (CHANGE ME)
    
base_url = 'https://www.googleapis.com/youtube/v3/search?'
api_key = 'AIzaSyDlITOYKP8ABriX7UZisXTF9DDtTfma480'

remainder = 'part=snippet&maxResults=' + str(results_per_page) +'&' + 'q=' + search_params + '&key=' + api_key
url = base_url + remainder

# To track number of additions to Database
count = 0

# scraping videos related to 'Grab'
# range is the the number of pages to search through
for i in range(num_pages):
    #opening the YouTube API
    http = urllib3.PoolManager(cert_reqs = 'CERT_REQUIRED', ca_certs=certifi.where())
    r = http.request('GET', url)
    response = r.data
    data = json.loads(response)
    items = data['items']
    next_page_token = data['nextPageToken']
    if next_page_token not in tokensSeen:
        tokensSeen.append(next_page_token)

    for item in items:
        if item['id']['kind'] == 'youtube#video' and item['id']['videoId'] not in seen:
            videoid = item['id']['videoId']
            video_id.append(videoid)
            snippet = item['snippet']
            title.append(snippet['title'])
            description.append(snippet['description'])
            published_at.append(snippet['publishedAt'])
            count += 1

    url = base_url + 'pageToken=' + str(next_page_token) + '&' + remainder

# formatting data
df = pd.DataFrame(published_at, columns = ['published_at'])
df['video_id']=video_id
df['title']=title
df['description']=description
# left a giant string here for future use :)

tokendf = pd.
'''
#translate data
translator = Translator()
translated = []
for row in df['title']:
    try:
        translated.append(translator.translate(row).text)
    except ValueError:
        translated.append('translate manually')

df['title_translated']=translated

#getting comments
comments = []
#get top rated comments for each video
for id in df['video_id']:
    dict = {}
    #adjust maxResults to liking
    video_link = 'https://www.googleapis.com/youtube/v3/commentThreads?maxResults=50&part=snippet%2C+replies&order=relevance&videoId=' + str(id) + '&key=' + api_key
    http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
    r = http.request('GET', video_link)
    response = r.data
    data = json.loads(response)
    items = data['items']

    for item in items:
        comment = item['snippet']['topLevelComment']['snippet']['textOriginal']
        channel_id = item['snippet']['topLevelComment']['snippet']['authorChannelId']['value']
        dict[channel_id]=[comment]
    for i, j in dict.items():
        #remove emojis
        row = ''.join(j)
        new_row = ''.join(c for c in row if c not in emoji.UNICODE_EMOJI)
        try:
            #translate
            translated = translator.translate(new_row).text
            dict[i].append(translated)
        except ValueError:
            dict[i].append('translate manually')
    comments.append(dict)

df['comments']=comments
'''


print(str(count) + " results added!")
df.to_csv('test.csv')