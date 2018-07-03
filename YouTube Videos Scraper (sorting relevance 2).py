import urllib3
import certifi
import json
import pandas as pd
from googletrans import Translator
import emoji
import webbrowser

df = pd.read_csv('/Users/claudia.seow/Desktop/youtubeScraper/langdetectBatch2.csv')

published_at = []
video_id = []
title = []
description = []
relevance = []
index = 1001
for id in df['EN_video_id'][1001: 1005]:
    webbrowser.open_new_tab('https://www.youtube.com/watch?v=' + str(id))
    value = input('relevance ')
    if value == 'na':
        index += 1
        continue
    else:
        published_at.append(df['EN_published_at'][index])
        video_id.append(df['EN_video_id'][index])
        title.append(df['EN_title'][index])
        description.append(df['EN_description'][index])
        relevance.append(value)
        index += 1

new_df = pd.DataFrame(published_at, columns = ['published_at'])
new_df['video_id'] = video_id
new_df['title'] = title
new_df['description'] = description
new_df['relevance'] = relevance

new_df.to_csv('/Users/claudia.seow/Desktop/youtubeScraper/relevanceBatch2.csv', index=False)
