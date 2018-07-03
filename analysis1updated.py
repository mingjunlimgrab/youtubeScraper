from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import pandas as pd
import nltk
import random

df = pd.read_csv("/Users/claudia.seow/Desktop/youtubeScraper/sorted02k.csv")

stop_words = {'who', 'all', 'very', 'can', "she's", 'did', 'hadn', 'they', "that'll", "you'll", 'through', 'than',
              'most', 'out', 'in', 'theirs', 'your', 'are', 'y', 'this', 'some', 'few', 'themselves', 'you', "won't",
              'against', 've', 'don', 'me', 'while', 'by', 'further', 'aren', 'wasn', 's', 'now', 'hers', 'on', 'was',
              'i', "haven't", 'shan', 'where', "mightn't", 'isn', 'were', 'once', 're', 'yourselves', 'or', 'if',
              "weren't", 'had', 'wouldn', 'it', 'ma', 'd', 'how', "should've", 'own', 'won', "you're", 'when', 'he',
              "needn't", 'does', 'been', 'these', 'itself', 'which', 'any', 'needn', 'its', 'what', 'there', 'my',
              'more', 'his', 'whom', 'him', "mustn't", 'down', 'the', 'she', 'both', 'hasn', 'ain', "shouldn't",
              'has', 'll', "wasn't", "hadn't", 'up', 'will', 'ours', 'yours', 'her', 'as', 'below', 'then', 'here',
              'for', "didn't", 'yourself', 'do', 'over', 'them', 'between', 'from', 'that', 't', 'with', 'being',
              "doesn't", "shan't", 'and', 'at', "you've", "hasn't", 'doesn', "couldn't", 'couldn', 'an', 'because',
              'before', 'each', 'nor', "it's", 'into', 'himself', 'have', "aren't", 'above', 'am', 'didn', 'just',
              'herself', 'after', 'why', 'shouldn', 'such', 'doing', 'too', "isn't", 'no', 'ourselves', "don't",
              'but', 'about', 'a', 'having', 'be', 'haven', 'm', 'of', 'to', 'myself', 'again', 'is', 'we', 'not',
              'our', 'mightn', 'only', 'so', 'under', 'other', 'their', "you'd", 'o', 'those', 'mustn', 'weren',
              'off', 'should', "wouldn't", 'until', 'same', 'during', '-', '(', ')', '|', ',', '[', ']', ':', '%', 'no'}

FLAG = {'perfidious', '8 ball pool', 'factorio', 'gameplay', 'pussy', 'trump', 'mall grab', 'grab lab', 'boob',
        'cash grab', 'ass grab', 'GTA', 'fallout 4', "smash'n'grab", 'grim dawn', 'minecraft', 'fortnite',
        'sonic', 'roblox', 'grab points', 'grab point', 'grabpoints', 'grabpoint', 'music video', 'hsn'}

SCORE_DICT = {'grabcar': 5, 'grabbike': 5, 'grabcycle': 5, 'grabfood': 5, 'grabtaxi':5, 'grabshuttle': 5,
'grabexpress':5, 'grabpay':5, 'justgrab':5, 'grab':2, 'uber':4, 'GOJEK': 4, 'ryde':4, 'mod': 3, 'driver': 4, 'drivers': 4, 'app': 3, 'car': 3, 'taxi': 4, 'job': 4, 'version': 2, 'delivery': 2,
'private': 1, 'hire': 2, 'singapore': 3, 'sg':3, 'malaysia':3, 'vietnam':2, 'vn': 2, 'philippines': 2, 'ph': 2, 'kuala':1, 'lumpur':1, 'promo':3, 'premium': 2,
'passenger': 4, 'bike': 4, 'gps': 3, 'spoof':3, 'hack':2, 'fake':2, 'rider': 4, 'cancel':3, 'cancellation':3, 'AR':3, 'pick': 2, 'order': 2, 'tutorial':1, 'tute':1, 'install':1, 'whatsapp': 3,
'download': 1, 'softban': 4, 'ban':3, 'banned':3, 'root': 3, 'booking':4, 'book':3, 'southeast': 3, 'asia':3, 'bypass':2, 'modification': 3, 'malaysian': 3, 'singaporean': 3, 'acceptance': 2, 'rate': 1, 'destination': 2
}

def dehypdeslash(title):
    result1 = title
    if '-' in result1:
        result1 = title.split('-')
        result1 = ' '.join(result1)
    if '/' in result1:
        result1 = result1.split('/')
        result1 = ' '.join(result1)
    return result1

def algorithm(args):
    if len(args)==0:
        val = 0
    if len(args)==1:
        val = args[0] * 1.5
    if len(args)==2:
        val = (args[0] * 1.5 + args[1] * 1.3) * 1.1
    if len(args)==3:
        val = (args[0] * 1.5 + args[1] * 1.3 + args[2] * 1.2) * 1.2
    if len(args)==4:
        val = (args[0] * 1.5 + args[1] * 1.3 + args[2] * 1.2 + args[3] * 1.1) * 1.3
    if len(args)>=5:
        val = (args[0] * 1.5 + args[1] * 1.3 + args[2] * 1.2 + args[3] * 1.1 + args[4] * 1.0) * 1.4
    if val >= 10:
        return 10
    else:
        return val

for title in df['title']:
    tokenized = []
    title = dehypdeslash(title)
    words = word_tokenize(title)
    for word in words:
        if word not in stop_words:
            tokenized.append(word.lower())
    keywords = {}
    for w in tokenized:
        if w in SCORE_DICT.keys():
            keywords[w]=SCORE_DICT[w]
    new_keywords = sorted(keywords, key=lambda x: keywords[x], reverse=True)
    final_keywords = {}
    for item in new_keywords:
        final_keywords[item] = keywords[item]
    args = []
    for i in final_keywords.values():
        args.append(i)
    print(title + '  ' + str(algorithm(args)))