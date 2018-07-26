import pandas as pd
import webbrowser
import csv
from mjutils import flagger, dehypdeslash, grabCheck

FLAG = {}

fileToRead = '/Users/mingjun.lim/Documents/youtubeScraper/Data/threat_data.csv'
fileToWrite = '/Users/mingjun.lim/Documents/youtubeScraper/Data/mjThreatLabelled.csv'
indexToStart = 560
nextIndexToWrite = 0

#Hotkeys
YES = '3'
NO = '4'
SHOW = '/'
EXIT = 'exit'
BACK = 'prev'
acceptable = [YES, NO, SHOW, EXIT, BACK]

def alreadyInitialized():
    # open 'English only' csv file
    df = pd.read_csv(fileToRead)
    rows = []
    index = indexToStart
    i = nextIndexToWrite
    for id in df['video_id'][index:]:
        newtitlething = dehypdeslash(df['title'][index])
        fleg = flagger(newtitlething.lower(), FLAG)
        row = []
        print(df['title'][index])
        value = False
        if not fleg:
            row.append(i)
            row.append(df['published_at'][index])
            row.append(df['video_id'][index])
            row.append(df['title'][index])
            row.append(df['description'][index])
            row.append(df['relevance'][index])
            row.append('LOW')
            rows.append(row)
            index += 1
            continue
        while value not in acceptable:
            print("--- Not Threat: " + NO + " --- Open Video: " + SHOW + " --- Threat: " + YES)
            value = input('relevance ')
        # open the link if you can't determine relevancy from title
        if value == BACK:
            rows.pop()
            index -= 1
            continue
        if value == EXIT:
            print('Stopping process at Index: ' + str(index))
            with open(fileToWrite, 'a') as file:
                writer = csv.writer(file)
                for j in rows:
                    try:
                        writer.writerow(j)
                    except:
                        continue
            return

        if value == SHOW:
            webbrowser.open_new_tab('https://www.youtube.com/watch?v=' + str(id))
            value = False
            while value not in acceptable:
                print(
                    "--- Not Threat: " + NO + " --- Open Video: " + SHOW + " --- Threat: " + YES)
                value = input(df['title'][index] + ' threat ')
            row.append(i)
            row.append(df['published_at'][index])
            row.append(df['video_id'][index])
            row.append(df['title'][index])
            row.append(df['description'][index])
            row.append(df['relevance'][index])
            if value == YES:
                row.append('HIG')
            else:
                row.append('LOW')
            rows.append(row)
            i += 1
            index += 1
        else:
            row.append(i)
            row.append(df['published_at'][index])
            row.append(df['video_id'][index])
            row.append(df['title'][index])
            row.append(df['description'][index])
            row.append(df['relevance'][index])
            if value == YES:
                row.append('HIG')
            else:
                row.append('LOW')
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


    indices = []
    published_at = []
    video_id = []
    title = []
    description = []
    relevance = []
    threat = []
    index = indexToStart #index to start from
    for id in df['video_id'][index:]:
        newtitlething = dehypdeslash(df['title'][index])
        fleg = flagger(newtitlething.lower(), FLAG) and grabCheck(newtitlething.lower())
        row = []
        print(df['title'][index])
        value = False
        if not fleg:
            published_at.append(df['published_at'][index])
            video_id.append(df['video_id'][index])
            title.append(df['title'][index])
            description.append(df['description'][index])
            relevance.append(df['relevance'][index])
            threat.append('HIG')

            index += 1
            continue
        while value not in acceptable:
            print("--- Not Threat: " + NO + " --- Open Video: " + SHOW + " --- Threat: " + YES)
            value = input('threat ')
        # open the link if you can't determine relevancy from title
        if value == EXIT:
            new_df = pd.DataFrame(published_at, columns=['published_at'])
            new_df['video_id'] = video_id
            new_df['title'] = title
            new_df['description'] = description
            new_df['relevance'] = relevance
            return

            new_df.to_csv((fileToWrite))
        if value == SHOW:
            webbrowser.open_new_tab('https://www.youtube.com/watch?v=' + str(id))
            value = False
            while not value:
                print(
                    "--- Not Threat: " + NO + " --- Open Video: " + SHOW + " --- Threat: " + YES)
                value = input(df['title'][index] + ' relevance ')
            published_at.append(df['published_at'][index])
            video_id.append(df['video_id'][index])
            title.append(df['title'][index])
            description.append(df['description'][index])
            relevance.append(df['relevance'][index])
            if value == YES:
                threat.append('HIG')
            else:
                threat.append('LOW')
            index += 1
        else:
            published_at.append(df['EN_published_at'][index])
            video_id.append(df['EN_video_id'][index])
            title.append(df['EN_title'][index])
            description.append(df['EN_description'][index])
            relevance.append(df['relevance'][index])
            if value == YES:
                relevance.append('HIG')
            else:
                relevance.append('LOW')
            index += 1
    # create new file
    new_df = pd.DataFrame(published_at, columns=['published_at'])
    new_df['video_id'] = video_id
    new_df['title'] = title
    new_df['description'] = description
    new_df['relevance'] = relevance
    new_df['threat'] = threat

    new_df.to_csv((fileToWrite))

#### MAIN ####
initializedOrNot = False
try:
    df = pd.read_csv(fileToRead)
    initializedOrNot = True
except:
    initializedOrNot = False

if initializedOrNot:
    print('already initialized but stil gonna start anyway')
    alreadyInitialized()
else:
    print('initializing!')
    initialization()

