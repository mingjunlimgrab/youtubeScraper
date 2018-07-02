import pandas as pd
import webbrowser
import csv

# Note: rest of the commented code that's unused is for initializing the process to create the file for the first time,
# then the rest of the rode that runs is to add into the file.

# open 'English only' csv file
df = pd.read_csv('/Users/claudia.seow/Desktop/youtubeScraper/langidBatch2.csv')

# published_at = []
# video_id = []
# title = []
# description = []
# relevance = []

# collecting new list of rows to append as rows to already created relevanceBatch2.csv
rows = []
index = 1951
i = 926
for id in df['EN_video_id'][1951: 2001]:
    row = []
    print(df['EN_title'][index])
    value = input('relevance ')
    # open the link if you can't determine relevancy from title
    if value == 'z':
        webbrowser.open_new_tab('https://www.youtube.com/watch?v=' + str(id))
        value = input(df['EN_title'][index] + ' relevance ')
        if value == 'na':
            index += 1
            continue
        else:
            row.append(i)
            row.append(df['EN_published_at'][index])
            row.append(df['EN_video_id'][index])
            row.append(df['EN_title'][index])
            row.append(df['EN_description'][index])
            row.append(value)
            rows.append(row)
            # published_at.append(df['EN_published_at'][index])
            # video_id.append(df['EN_video_id'][index])
            # title.append(df['EN_title'][index])
            # description.append(df['EN_description'][index])
            # relevance.append(value)
            i+=1
            index += 1
    # video not in English
    elif value == 'na':
        index += 1
        continue
    else:
        row.append(i)
        row.append(df['EN_published_at'][index])
        row.append(df['EN_video_id'][index])
        row.append(df['EN_title'][index])
        row.append(df['EN_description'][index])
        row.append(value)
        rows.append(row)
        i += 1
        index += 1

# opens relevanceBatch2.csv and appends in the newly collected rows
with open('/Users/claudia.seow/Desktop/youtubeScraper/relevanceBatch2.csv', 'a') as file:
    writer = csv.writer(file)
    for j in rows:
        try:
            writer.writerow(j)
        except:
            continue

# create new file
# new_df = pd.DataFrame(published_at, columns = ['published_at'])
# new_df['video_id'] = video_id
# new_df['title'] = title
# new_df['description'] = description
# new_df['relevance'] = relevance

#new_df.to_csv(('/Users/claudia.seow/Desktop/youtubeScraper/relevanceBatch2.csv'))