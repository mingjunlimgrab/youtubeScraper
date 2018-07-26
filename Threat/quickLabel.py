import pandas as pd
import webbrowser
import csv
from mjutils import flagger, dehypdeslash, grabCheck

FLAG = {}

fileToRead = '/Users/mingjun.lim/Documents/youtubeScraper/Data/zeros.csv'
fileToWrite = '/Users/mingjun.lim/Documents/youtubeScraper/Data/testThreatLabelledFull.csv'

df = pd.read_csv(fileToRead)
threat = []
for index in range(len(df['title'])):
    threat.append('LOW')

new_df = pd.DataFrame(df['published_at'], columns=['published_at'])
new_df['video_id'] = df['video_id']
new_df['title'] = df['title']
new_df['description'] = df['description']
new_df['relevance'] = df['relevance']
new_df['threat'] = threat

new_df.to_csv((fileToWrite))