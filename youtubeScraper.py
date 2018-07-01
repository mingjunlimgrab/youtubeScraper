import urllib3
import certifi
import json
import pandas as pd
import emoji


# import textblob

def remove_stuff(text, list_of_stuff):
    return ''.join([x for x in text if x not in list_of_stuff])


def remove_emoji(text):
    return remove_stuff(text, emoji.UNICODE_EMOJI)


############################## START OF MAIN FUNCTION #######################################

# Modifyable search parameters (CHANGE ME)
search_params = 'Grab+mod+app'  # Params seperated by + (eg. ‘Grab+fake+app’ or ‘Grab+tutorial’)
num_pages = 1000
results_per_page = 50
page_to_start = False # set to False if start from page 1
# Modifyable search parameters (CHANGE ME)

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
    tokn = pd.read_csv('tokensSeen.csv')
    print('managed to load!')
    tolkien = tokn['0']
    tokensSeen = tolkien.tolist()
except:
    print('tokens seen not found')
    tokensSeen = []

base_url = 'https://www.googleapis.com/youtube/v3/search?'
api_key = 'AIzaSyDlITOYKP8ABriX7UZisXTF9DDtTfma480'

remainder = 'part=snippet&maxResults=' + str(results_per_page) + '&' + 'q=' + search_params + '&key=' + api_key
if not page_to_start:
    url = base_url + remainder
else:
    url = base_url + 'pageToken=' + str(page_to_start or tokensSeen[-1] ) + '&' + remainder

# To track number of additions to Database
count = 0
tokenCount = 0
pagesScanned = 0

# scraping videos related to 'Grab'
# range is the the number of pages to search through
for i in range(num_pages):
    # opening the YouTube API
    try:
        http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
        r = http.request('GET', url)
        response = r.data
        data = json.loads(response)
        items = data['items']
        next_page_token = data['nextPageToken']
        if next_page_token not in tokensSeen:
            tokensSeen.append(next_page_token)
            tokenCount += 1

        for item in items:
            if item['id']['kind'] == 'youtube#video' and item['id']['videoId'] not in seen:
                videoid = item['id']['videoId']
                video_id.append(videoid)
                snippet = item['snippet']
                title.append(remove_emoji(snippet['title']))
                description.append(remove_emoji(snippet['description']))
                published_at.append(snippet['publishedAt'])
                count += 1

        url = base_url + 'pageToken=' + str(next_page_token) + '&' + remainder
        pagesScanned += 1
    except:
        break

# formatting data
df = pd.DataFrame(published_at, columns=['published_at'])
df['video_id'] = video_id
df['title'] = title
df['description'] = description

tokendf = pd.DataFrame(tokensSeen)
tokendf.to_csv('tokensSeen.csv')
print(str(tokenCount) + " tokens added!")
print(str(count) + " results added!")
print(str(pagesScanned) + ' pages Scanned!')
df.to_csv('test.csv')
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
