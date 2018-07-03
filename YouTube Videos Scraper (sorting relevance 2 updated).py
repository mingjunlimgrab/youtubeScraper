import pandas as pd
import webbrowser
import csv

fileToRead = 'langidBatch2.csv'
fileToWrite = 'mjRelevance1.csv'
indexToStart = 1951
indexToEnd = 2001
nextIndexToWrite = 0

def alreadyInitialized():
    # open 'English only' csv file
    df = pd.read_csv(fileToRead)
    rows = []
    index = indexToStart
    i = nextIndexToWrite
    for id in df['EN_video_id'][index: indexToEnd]:
        row = []
        print(df['EN_title'][index])
        value = False
        while not value:
            print("Not English: 'n' --- Not Grab: '0' --- Open Video: 'z' --- GRAB: '1'" )
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
                i += 1
                index += 1
        elif value == 'n':
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
    with open(fileToWrite, 'a') as file:
        writer = csv.writer(file)
        for j in rows:
            try:
                writer.writerow(j)
            except:
                continue

def initialization():
    df = pd.read_csv(fileToRead)

    published_at = []
    video_id = []
    title = []
    description = []
    relevance = []
    index = 1951 #index to start from
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
                published_at.append(df['EN_published_at'][index])
                video_id.append(df['EN_video_id'][index])
                title.append(df['EN_title'][index])
                description.append(df['EN_description'][index])
                relevance.append(value)
                i += 1
                index += 1
        elif value == 'na':
            index += 1
            continue
        else:
            published_at.append(df['EN_published_at'][index])
            video_id.append(df['EN_video_id'][index])
            title.append(df['EN_title'][index])
            description.append(df['EN_description'][index])
            relevance.append(value)
            index += 1
    # create new file
    new_df = pd.DataFrame(published_at, columns=['published_at'])
    new_df['video_id'] = video_id
    new_df['title'] = title
    new_df['description'] = description
    new_df['relevance'] = relevance

    new_df.to_csv((fileToWrite))

#### MAIN ####

initialization()