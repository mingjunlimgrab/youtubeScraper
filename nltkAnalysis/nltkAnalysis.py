import nltk
import random
import pandas as pd
from nltk.tokenize import word_tokenize
import pickle

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

# wb - write, rb - read
f = open('my_classifier.pickle', 'rb')
wf = open('word_features.pickle', 'rb')
classifier = pickle.load(f)
word_features = pickle.load(wf)

def dehypdeslash(title):
    result1 = title
    if '-' in result1:
        result1 = title.split('-')
        result1 = ' '.join(result1)
    if '/' in result1:
        result1 = result1.split('/')
        result1 = ' '.join(result1)
    return result1

def clean(title):
    tokenize = []
    title = dehypdeslash(title)
    words = word_tokenize(title)
    for word in words:
        lowercase_word = word.lower()
        if lowercase_word not in stop_words:
            tokenize.append(lowercase_word)
    return tokenize

def document_features(doc):
    doc_words = set(doc)
    features = {}
    for (word, freq) in word_features:
        features['contains({})'.format(word)] = (word in doc_words)
    return features

# df = pd.read_csv("/Users/claudia.seow/PycharmProjects/new/sorted_data.csv")
#
# documents = []
# lib = []
# index = 0
# for title in df['title']:
#     tokenize = []
#     title = dehypdeslash(title)
#     words = word_tokenize(title)
#     for word in words:
#         lowercase_word = word.lower()
#         if lowercase_word not in stop_words:
#             tokenize.append(lowercase_word)
#             lib.append(lowercase_word)
#     documents.append((tokenize, df['relevance'][index]))
#     index += 1

# option 1 splits data 'evenly'
# rel = []
# irr = []
# for item in documents:
#     if item[1] == 1:
#         rel.append(item)
#     else:
#         irr.append(item)
#
# random.shuffle(rel)
# random.shuffle(irr)
#
# all_words = nltk.FreqDist(w for w in lib)
# word_features = list(all_words.most_common(2000))
#
# rel_featuresets = [(document_features(d), c) for (d, c) in rel]
# irr_featuresets = [(document_features(d), c) for (d, c) in irr]
#
# train_set = rel_featuresets[:373] + irr_featuresets[:10418]
# test_set = rel_featuresets[373:] + irr_featuresets[10418:]

# option 2 shuffles data without splitting
# random.shuffle(documents)
# all_words = nltk.FreqDist(w for w in lib)
# word_features = list(all_words.most_common(2000))
# featuresets = [(document_features(d), c) for (d, c) in documents]
# train_set, test_set = featuresets[:12000], featuresets[12000:]

# trains data and prints accuracy
# classifier = nltk.NaiveBayesClassifier.train(train_set)
# print(nltk.classify.accuracy(classifier, test_set))
# classifier.show_most_informative_features(5)

def predictor(titles):
    for title in titles:
        cleaned = clean(title)
        print(title + ' ' + str(classifier.classify(document_features(cleaned))))

predicting_titles = ['Man has 156 seconds to grab free stuff', 'Grab Mod 3.2',
                     'What it\'s like to be a Grabcar Driver', 'Grab driver mod 5.31.4',
                     'Uber Agrees to Sell Southeast Asian Operations to Rival Grab', 'grab gps tutorial']

predictor(predicting_titles)

# for loading in data
# pickle.dump(classifier, f)
# pickle.dump(word_features, wf)

f.close()
wf.close()