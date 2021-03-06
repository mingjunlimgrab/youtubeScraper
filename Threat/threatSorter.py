import pandas as pd
import webbrowser
import csv

fileToRead = '/Users/mingjun.lim/Documents/youtubeScraper/Data/testThreatLabelledFull.csv'
fileToWrite = '/Users/mingjun.lim/Documents/youtubeScraper/Data/testThreatSorted.csv'

df = pd.read_csv(fileToRead)

one_published_at = []
one_video_id = []
one_title = []
one_description = []
one_relevance = []
one_threat = []

zero_published_at = []
zero_video_id = []
zero_title = []
zero_description = []
zero_relevance = []
zero_threat = []

index = 0

for index in range(len(df['title'])):
    if df['threat'][index] == 'HIG':
        one_published_at.append(df['published_at'][index])
        one_video_id.append(df['video_id'][index])
        one_title.append(df['title'][index])
        one_description.append(df['description'][index])
        one_relevance.append(df['relevance'][index])
        one_threat.append(df['threat'][index])
        print(df['title'][index])
    else:
        zero_published_at.append(df['published_at'][index])
        zero_video_id.append(df['video_id'][index])
        zero_title.append(df['title'][index])
        zero_description.append(df['description'][index])
        zero_relevance.append(df['relevance'][index])
        zero_threat.append(df['threat'][index])

num_ones = len(one_video_id)
num_zeros = len(zero_video_id)
percentYield = (num_ones * 100)/(num_ones + num_zeros)
print(percentYield)

#Combinations:
zero_published_at.extend(one_published_at)
zero_video_id.extend(one_video_id)
zero_title.extend(one_title)
zero_description.extend(one_description)
zero_relevance.extend(one_relevance)
zero_threat.extend(one_threat)

new_df = pd.DataFrame(zero_published_at, columns=['published_at'])
new_df['video_id'] = zero_video_id
new_df['title'] = zero_title
new_df['description'] = zero_description
new_df['relevance'] = zero_relevance
new_df['threat'] = zero_threat

new_df.to_csv((fileToWrite))

# one_published_at.extend(zero_published_at)
# one_video_id.extend(zero_video_id)
# one_title.extend(zero_title)
# one_description.extend(zero_description)
# one_relevance.extend(zero_relevance)
#
# new_df = pd.DataFrame(one_published_at, columns=['published_at'])
# new_df['video_id'] = one_video_id
# new_df['title'] = one_title
# new_df['description'] = one_description
# new_df['relevance'] = one_relevance
#
# print("total rows added is " + str(len(new_df['title'])))
# print("number of relevant results: " + str(num_ones))
# print("number of irrelevant results: " + str(num_zeros))
# print("percent of relevant videos: " + str(percentYield))
#
# new_df.to_csv((fileToWrite))

