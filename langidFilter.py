import csv
import pandas as pd
import langid

#Parameters#
fileToRead = 'grab+app+mod.csv'
fileToWrite = 'EN_videos.csv'
df = pd.read_csv(fileToRead)

EN_published_at = []
EN_video_id = []
EN_title = []
EN_description = []

index = 0
for title in df['title']:
    try:
        term = title + ' ' + df['description'][index]
        print(term)
        if langid.classify(title)[0] == 'en':
            EN_published_at.append(df['published_at'][index])
            EN_video_id.append(df['video_id'][index])
            EN_title.append(df['title'][index])
            EN_description.append(df['description'][index])
        index += 1
    except:
        index += 1


# '''
# i = 0
# while i <=480:
#     published_at = df['published_at'][i]
#     video_id = df['video_id'][i]
#     title = df['title'][i]
#     description = df['description'][i]
#     if langdetect.detect(title) == 'en':
#         EN_published_at.append(published_at)
#         EN_video_id.append(video_id)
#         EN_title.append(title)
#         EN_description.append(description)
#     i += 1
# '''

EN_df = pd.DataFrame(EN_published_at, columns = ['EN_published_at'])
EN_df['EN_video_id']=EN_video_id
EN_df['EN_title']=EN_title
EN_df['EN_description']=EN_description

EN_df.to_csv(fileToWrite)