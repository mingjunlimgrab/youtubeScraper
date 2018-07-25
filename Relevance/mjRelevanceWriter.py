import pandas as pd
import webbrowser
import csv
from mjutils import flagger, dehypdeslash, grabCheck

FLAG = {'perfidious', '8 ball pool', 'factorio', 'gameplay', 'pussy', 'trump', 'mall grab', 'grab lab', 'boob', 'grab knife', 'grab it now', 'grab bag',
        'cash grab', 'ass grab', 'GTA', 'fallout 4', "smash'n'grab", 'grim dawn', 'minecraft', 'fortnite', 'grab and go', 'grab the bottle', 'land grab',
        'sonic', 'roblox', 'grab points', 'grab point', 'grabpoints', 'grabpoint', 'music video', 'hsn', 'grab the bottle', 'smash and grab'}

fileToRead = '/Users/mingjun.lim/Documents/youtubeScraper/Data/languageFilteredData/validationBatch2EN.csv'
fileToWrite = '/Users/mingjun.lim/Documents/youtubeScraper/Data/manuallyClassifiedData/validationBatchLabelled.csv'
indexToStart = 1500
indexToEnd = 2245
nextIndexToWrite = 0

#Hotkeys
YES = '3'
NO = '4'
NOTENG = 'c'
SHOW = '/'
EXIT = 'exit'
BACK = 'prev'
acceptable = [YES, NO, NOTENG, SHOW, EXIT, BACK]

def alreadyInitialized():
    # open 'English only' csv file
    df = pd.read_csv(fileToRead)
    rows = []
    index = indexToStart
    i = nextIndexToWrite
    for id in df['video_id'][index: indexToEnd]:
        newtitlething = dehypdeslash(df['title'][index])
        fleg = flagger(newtitlething.lower(), FLAG) and grabCheck(newtitlething.lower())
        row = []
        print(df['title'][index])
        value = False
        if not fleg:
            row.append(i)
            row.append(df['published_at'][index])
            row.append(df['video_id'][index])
            row.append(df['title'][index])
            row.append(df['description'][index])
            row.append('0')
            rows.append(row)
            index += 1
            continue
        while value not in acceptable:
            print("Not English:" + NOTENG + " --- Not Grab: " + NO + " --- Open Video: " + SHOW + " --- GRAB: " + YES )
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
                    "Not English:" + NOTENG + " --- Not Grab: " + NO + " --- Open Video: " + SHOW + " --- GRAB: " + YES)
                value = input(df['title'][index] + ' relevance ')
            if value == NOTENG:
                index += 1
                continue
            else:
                row.append(i)
                row.append(df['published_at'][index])
                row.append(df['video_id'][index])
                row.append(df['title'][index])
                row.append(df['description'][index])
                if value == YES:
                    row.append('1')
                else:
                    row.append('0')
                rows.append(row)
                i += 1
                index += 1
        elif value == NOTENG:
            index += 1
            continue
        else:
            row.append(i)
            row.append(df['published_at'][index])
            row.append(df['video_id'][index])
            row.append(df['title'][index])
            row.append(df['description'][index])
            if value == YES:
                row.append('1')
            else:
                row.append('0')
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
    index = indexToStart #index to start from
    for id in df['video_id'][index: indexToEnd]:
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
            relevance.append('0')
            index += 1
            continue
        while value not in acceptable:
            print("Not English:" + NOTENG + " --- Not Grab: " + NO + " --- Open Video: " + SHOW + " --- GRAB: " + YES)
            value = input('relevance ')
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
                    "Not English:" + NOTENG + " --- Not Grab: " + NO + " --- Open Video: " + SHOW + " --- GRAB: " + YES)
                value = input(df['title'][index] + ' relevance ')
            if value == NOTENG:
                index += 1
                continue
            else:
                published_at.append(df['published_at'][index])
                video_id.append(df['video_id'][index])
                title.append(df['title'][index])
                description.append(df['description'][index])
                if value == YES:
                    relevance.append('1')
                else:
                    relevance.append('0')
                index += 1
        elif value == NOTENG:
            index += 1
            continue
        else:
            published_at.append(df['published_at'][index])
            video_id.append(df['video_id'][index])
            title.append(df['title'][index])
            description.append(df['description'][index])
            if value == YES:
                relevance.append('1')
            else:
                relevance.append('0')
            index += 1
    # create new file
    new_df = pd.DataFrame(published_at, columns=['published_at'])
    new_df['video_id'] = video_id
    new_df['title'] = title
    new_df['description'] = description
    new_df['relevance'] = relevance

    new_df.to_csv((fileToWrite))

#### MAIN ####
initializedOrNot = False
try:
    df = pd.read_csv(fileToRead)
    initializedOrNot = True
except:
    initializedOrNot = False

if initializedOrNot:
    alreadyInitialized()
else:
    initialization()

