import requests
import json
import urllib3
import certifi

#YouTube Search
base_url = 'https://www.googleapis.com/youtube/v3/search?'
api_key = 'AIzaSyDlITOYKP8ABriX7UZisXTF9DDtTfma480'
#settings CHANGE ME
numberOfPagesToSearch = 1 #change me
searchParameter = 'Grab' #change me
maxResultsPerPage = 10 #change me
#settings CHANGE ME
# remainder = 'part=snippet&maxResults=' + str(maxResultsPerPage) + '&' + 'q=' + searchParameter + '&key=' + api_key
# url = base_url + remainder
# http = urllib3.PoolManager(cert_reqs = 'CERT_REQUIRED', ca_certs=certifi.where())
# r = http.request('GET', url)
# response = r.data
# data = json.loads(response)
id = "O_mGWr3LN7s"
video_link = 'https://www.googleapis.com/youtube/v3/commentThreads?maxResults=50&part=snippet%2C+replies&order=relevance&videoId=' + str(id) + '&key=' + api_key
http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
r = http.request('GET', video_link)
response = r.data
data = json.loads(response)

with open("comments_file.json", "w") as data_file:
	json.dump(data, data_file, indent=2)


# load_json = open('data_file.json', 'r')
# new_todos = json.load(load_json)
# print(type(new_todos))
# new_todos[0]["id"] = 45000000

# with open('data_file.json', 'w') as jsonFile:
# 	deta = json.dumps(new_todos, indent=4, separators=(',', ': '))
	# jsonFile.write(deta)