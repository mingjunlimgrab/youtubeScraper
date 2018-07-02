import urllib3
import certifi
import json
import pandas as pd
from googletrans import Translator
import emoji
import webbrowser

df = pd.read_csv('/Users/claudia.seow/Desktop/youtubeScraper/langdetectBatch2.csv')

relevance = []

for id in df['EN_video_id'][1001: 1050]:
    webbrowser.open_new_tab('https://www.youtube.com/watch?v=' + str(id))
    value = input('relevance ')
    if value == 'na':
        continue
    else:
        relevance.append(value)
df['relevance']=relevance

df.to_excel('/Users/claudia.seow/Desktop/youtubeScraper/relevanceBatch2', index=False)
