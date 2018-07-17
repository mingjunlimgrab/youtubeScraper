from nltk.tokenize import word_tokenize
import pickle
import random
import pandas as pd
import numpy as np
from nltkAnalysis.VoteClassifier import VoteClassifier

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

c = open('nltkAnalysis/my_classifier.pickle', 'rb')
mnb = open('nltkAnalysis/MNB_classifier.pickle', 'rb')
bnb = open('nltkAnalysis/BernoulliNB_classifier.pickle', 'rb')
lg = open('nltkAnalysis/LogisticRegression_classifier.pickle', 'rb')
sgd = open('nltkAnalysis/SGD_classifier.pickle', 'rb')
svc = open('nltkAnalysis/SVC_classifier.pickle', 'rb')
lsvc = open('nltkAnalysis/LinearSVC_classifier.pickle', 'rb')
vc = open('nltkAnalysis/VoteClassifier.pickle', 'rb')
wf = open('nltkAnalysis/word_features.pickle', 'rb')

classifier = pickle.load(c)
MNB_classifier = pickle.load(mnb)
BernoulliNB_classifier = pickle.load(bnb)
LogisticRegression = pickle.load(lg)
SGD_classifier = pickle.load(sgd)
SVC_classifier = pickle.load(svc)
LinearSVC_classifier = pickle.load(lsvc)
vote_classifier = pickle.load(vc)
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

def append_truth_predictor(csvFileName, fileToWrite, classifier):
    df = pd.read_csv(csvFileName)
    titlesWithRelevance = df['title']
    relevance = []
    for title in titlesWithRelevance:
        cleaned = clean(title)
        d_f = document_features(cleaned)
        featurized = {}
        for feature in d_f:
            if d_f[feature] == True:
                featurized[feature] = True
        relevance.append(classifier.classify(featurized))

    published_at = df['published_at']
    video_id = df['video_id']
    title = df['title']
    description = df['description']

    new_df = pd.DataFrame(published_at, columns=['published_at'])
    new_df['video_id'] = video_id
    new_df['title'] = title
    new_df['description'] = description
    new_df['relevance'] = relevance

    new_df.to_csv((fileToWrite))

append_truth_predictor('languageFilteredData/langidBatch4.csv', 'autoTested2.csv', LinearSVC_classifier)