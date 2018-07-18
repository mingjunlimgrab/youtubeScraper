import urllib3
import certifi
import json
import pandas as pd
import emoji
import rfc3339
import datetime
from urllib.parse import quote_plus


# import textblob

def remove_stuff(text, list_of_stuff):
    return ''.join([x for x in text if x not in list_of_stuff])


def remove_emoji(text):
    return remove_stuff(text, emoji.UNICODE_EMOJI)


############################## START OF MAIN FUNCTION #######################################

# Modifyable search parameters (CHANGE ME)
search_params = 'Grab'  # Params seperated by + (eg. ‘Grab+fake+app’ or ‘Grab+tutorial’)
num_pages = 20
results_per_page = 50

time_delta = 15 # Days between each search frame
periods = 48 # Total time searched = periods * time_delta days before today's date.

writeFile = 'rawVideoData/grab4.csv'
readFile = 'rawVideoData/grab.csv'
# Modifyable search parameters (CHANGE ME)

# Load existing DataFrame (named test.csv). If unable to find, start from scratch.
old_df = pd.read_csv(readFile)
video_id = (old_df['video_id']).tolist()
seen = set(video_id)
video_id = []
title = []
description = []
published_at = []

base_url = 'https://www.googleapis.com/youtube/v3/search?'
api_key = 'AIzaSyDlITOYKP8ABriX7UZisXTF9DDtTfma480'

remainder = 'part=snippet&maxResults=' + str(results_per_page) + '&q=' + search_params + '&key=' + api_key
timenow = datetime.date.today()
deltatime = datetime.timedelta(days=time_delta)
nexttime = timenow - deltatime
publishedBefore = quote_plus(rfc3339.rfc3339(timenow))
publishedAfter = quote_plus(rfc3339.rfc3339(nexttime))
timeinfo = '&publishedBefore=' + publishedBefore + '&publishedAfter=' + publishedAfter

url = base_url + remainder + timeinfo

# To track number of additions to Database
count = 0
tokenCount = 0
pagesScanned = 0


# scraping videos related to 'Grab'
# range is the the number of pages to search through
for z in range(periods):
    for i in range(num_pages):
        # opening the YouTube API
        try:
            http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
            print(url)
            r = http.request('GET', url)
            response = r.data
            data = json.loads(response)
            items = data['items']
            next_page_token = data['nextPageToken']

            for item in items:
                if item['id']['kind'] == 'youtube#video' and item['id']['videoId'] not in seen:
                    videoid = item['id']['videoId']
                    video_id.append(videoid)
                    snippet = item['snippet']
                    title.append(remove_emoji(snippet['title']))
                    description.append(remove_emoji(snippet['description']))
                    published_at.append(snippet['publishedAt'])
                    count += 1

            url = base_url + 'pageToken=' + str(next_page_token) + timeinfo + '&' + remainder
            pagesScanned += 1
        except:
            break
    nexttime = nexttime - deltatime
    timenow = timenow - deltatime
    publishedBefore = quote_plus(rfc3339.rfc3339(timenow))
    publishedAfter = quote_plus(rfc3339.rfc3339(nexttime))
    timeinfo = '&publishedBefore=' + publishedBefore + '&publishedAfter=' + publishedAfter
    url = base_url + remainder + timeinfo

# formatting data
df = pd.DataFrame(published_at, columns=['published_at'])
df['video_id'] = video_id
df['title'] = title
df['description'] = description

print(str(count) + " results added!")
print(str(pagesScanned) + ' pages Scanned!')
df.to_csv(writeFile)

################################ END OF MAIN FUNCTION ################################


# Annex
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
