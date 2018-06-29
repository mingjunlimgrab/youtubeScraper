import urllib3
import certifi
import json
import requests

base_url = 'https://www.googleapis.com/youtube/v3/search?'
api_key = 'AIzaSyDlITOYKP8ABriX7UZisXTF9DDtTfma480'


def findVideos():
    try:
        data_dump = open("data_dump.json", "r")
        data_index = json.loads(data_dump)
    except:
        print('No data_dump found')
        print('Will initialize data_dump.json file on completion')
        data_dump = {}

    #settings CHANGE ME
    numberOfPagesToSearch = 1 #change me
    searchParameter = 'Grab' #change me
    maxResultsPerPage = 10 #change me
    firstXComments = 1 #change me
    #settings CHANGE ME

    remainder = 'part=snippet&maxResults=' + str(maxResultsPerPage) + '&' + 'q=' + searchParameter + '&key=' + api_key
    url = base_url + remainder

    video_id = []
    title = []
    published_at = []

    #scraping videos related to 'Grab'
    #range is the the number of pages to search through
    for i in range(numberOfPagesToSearch):
        #opening the YouTube API
        http = urllib3.PoolManager(cert_reqs = 'CERT_REQUIRED', ca_certs=certifi.where())
        r = http.request('GET', url)
        response = r.data
        data = json.loads(response)
        items = data['items']
        next_page_token = data['nextPageToken']

        for item in items:
            if item['id']['kind'] == 'youtube#video' and item['id']['videoId'] not in data_dump:
                videoid = item['id']['videoId']
                snippet = item['snippet']
                title = snippet['title']
                description = snippet['description']
                published_at = snippet['publishedAt']
                channelTitle = snippet['channelTitle']
                channelId = snippet['channelId']
                dataItem = {'title': title, 'description': description, 'published_at': published_at, "channelTitle": channelTitle, 'channelId':channelId}
                data_dump[videoid] = dataItem

                video_link = 'https://www.googleapis.com/youtube/v3/commentThreads?maxResults=50&part=snippet%2C+replies&order=relevance&videoId=' + str(videoid) + '&key=' + api_key
                http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
                r2 = http.request('GET', video_link)
                response2 = r2.data
                data2 = json.loads(response)
                items2 = data2['items']
                comments = {}
                #Only searches main comments (NOT REPLIES)
                for i in range(firstXComments):
                    thread = items2[i]
                    print(thread)
                    commentId = thread['id']
                    topComment = thread['snippet']["topLevelComment"]['snippet']
                    authorDisplayName = topComment["authorDisplayName"]
                    authorChannelId = topComment['authorChannelId']['value']
                    textOriginal = topComment['textOriginal']
                    comment = {'authorDisplayName': authorDisplayName, 'authorChannelId': authorChannelId,'textOriginal': textOriginal}
                    comments[commentId] = comment
                    if i == len(items2) - 1:
                        break
                data_dump[videoid]['comments'] = comments

        url = base_url + 'pageToken=' + str(next_page_token) + '&' + remainder


    with open("data_dump.json", "w+") as data_file:
        json.dump(data_dump, data_file, indent=4)

    return

#defunct
# def findComments(fileToScrape):
#     try:
#         data_dump = open(fileToScrape, "r")
#         data_index = json.loads(data_dump)
#     except:
#         print('No data_dump found ----- Aborting')
#         return
#     #Determine how many comments per video to obtain    
#     firstXComments = 20 #change me

#     for id in data_index:
#         video_link = 'https://www.googleapis.com/youtube/v3/commentThreads?maxResults=50&part=snippet%2C+replies&order=relevance&videoId=' + str(id) + '&key=' + api_key
#         http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
#         r = http.request('GET', video_link)
#         response = r.data
#         data = json.loads(response)
#         items = data['items']
#         comments = {}
#         #Only searches main comments (NOT REPLIES)
#         for i in range(firstXComments):
#             thread = items[i]
#             commentId = thread['id']
#             topComment = thread['snippet']['topLevelComment']['snippet']
#             authorDisplayName = topComment["authorDisplayName"]
#             authorChannelId = topComment['authorChannelId']['value']
#             textOriginal = topComment['textOriginal']
#             comment = {'authorDisplayName': authorDisplayName, 'authorChannelId': authorChannelId,'textOriginal': textOriginal}
#             comments[commentId] = comment
#         data_index[id]['comments'] = comments

#     with open(fileToScrape, "w+") as data_file:
#         json.dump(data_dump, data_file, indent=4)

findVideos()
#findComments('data_dump.json')


