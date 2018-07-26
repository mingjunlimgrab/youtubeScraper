import csv
import pandas as pd

df = pd.read_csv('threat_data_sorted.csv').sample(frac=1)


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
        one_relevance.append(1)
        one_threat.append('HIG')
        print(df['title'][index])
    else:
        zero_published_at.append(df['published_at'][index])
        zero_video_id.append(df['video_id'][index])
        zero_title.append(df['title'][index])
        zero_description.append(df['description'][index])
        zero_relevance.append(0)
        zero_threat.append('LOW')

test_published_at = []
test_video_id = []
test_title = []
test_description = []
test_relevance = []
test_threat = []

non_published_at = []
non_video_id = []
non_title = []
non_description = []
non_relevance = []
non_threat = []


fifteenone = int(len(one_published_at) * 0.15)
index = 0
for thing in one_published_at[:fifteenone]:
    test_published_at.append(thing)
    test_video_id.append(one_video_id[index])
    test_title.append(one_title[index])
    test_description.append(one_description[index])
    test_relevance.append(one_relevance[index])
    test_threat.append(one_threat[index])
    index += 1

for thing in one_published_at[fifteenone:]:
    non_published_at.append(thing)
    non_video_id.append(one_video_id[index])
    non_title.append(one_title[index])
    non_description.append(one_description[index])
    non_relevance.append(one_relevance[index])
    non_threat.append(one_threat[index])
    index += 1

nonfifteenone = int(len(zero_published_at) * 0.15)
index = 0
for thing in zero_published_at[:nonfifteenone]:
    test_published_at.append(thing)
    test_video_id.append(zero_video_id[index])
    test_title.append(zero_title[index])
    test_description.append(zero_description[index])
    test_relevance.append(zero_relevance[index])
    test_threat.append(zero_threat[index])
    index += 1

for thing in zero_published_at[nonfifteenone:]:
    non_published_at.append(thing)
    non_video_id.append(zero_video_id[index])
    non_title.append(zero_title[index])
    non_description.append(zero_description[index])
    non_relevance.append(zero_relevance[index])
    non_threat.append(zero_threat[index])
    index += 1

test_df = pd.DataFrame(test_published_at, columns=['published_at'])
test_df['video_id'] = test_video_id
test_df['title'] = test_title
test_df['description'] = test_description
test_df['relevance'] = test_relevance
test_df['threat'] = test_threat

train_df = pd.DataFrame(non_published_at, columns=['published_at'])
train_df['video_id'] = non_video_id
train_df['title'] = non_title
train_df['description'] = non_description
train_df['relevance'] = non_relevance
train_df['threat'] = non_threat


fileToWrite1 = 'test_threat_data.csv'
fileToWrite2 = 'validtrain_threat_data.csv'
test_df.to_csv((fileToWrite1))
train_df.to_csv((fileToWrite2))