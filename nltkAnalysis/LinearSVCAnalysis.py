import nltk
import random
import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.naive_bayes import MultinomialNB, BernoulliNB
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.svm import SVC, LinearSVC
from nltkAnalysis.VoteClassifier import VoteClassifier
import numpy as np
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

lsvc = open('LinearSVC_classifier.pickle', 'wb')
wf = open('word_features.pickle', 'wb')
tr = open('train_set.pickle', 'wb')
te = open('test_set.pickle', 'wb')



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

df = pd.read_csv("sorted_data.csv")

documents = []
lib = []
index = 0
for title in df['title']:
    tokenize = []
    title = dehypdeslash(title)
    words = word_tokenize(title)
    for word in words:
        lowercase_word = word.lower()
        if lowercase_word not in stop_words:
            tokenize.append(lowercase_word)
            lib.append(lowercase_word)
    documents.append([title, tokenize, df['relevance'][index]])
    index += 1

# option 1 splits data 'evenly'
rel = []
irr = []
for item in documents:
    if item[2] == 1:
        rel.append(item)
    else:
        irr.append(item)

random.shuffle(rel)
random.shuffle(irr)

all_words = nltk.FreqDist(w for w in lib)
word_features = list(all_words.most_common(3000))
rel_featuresets = [[item[0], (document_features(item[1]), item[2])] for item in rel]
irr_featuresets = [[item[0], (document_features(item[1]), item[2])] for item in irr]

twentyRel = int(len(rel_featuresets) * 0.2)
twentyIrr = int(len(irr_featuresets) * 0.2)
train_set_save = rel_featuresets[twentyRel:] + irr_featuresets[twentyIrr:]
test_set_save = rel_featuresets[:twentyRel] + irr_featuresets[:twentyIrr]

train_set = [item[1] for item in train_set_save]
test_set = [item[1] for item in test_set_save]

train_set_save_final = [[item[0], item[1][1]] for item in train_set_save]
test_set_save_final = [[item[0], item[1][1]] for item in test_set_save]

# option 2 shuffles data without splitting
# random.shuffle(documents)
# all_words = nltk.FreqDist(w for w in lib)
# word_features = list(all_words.most_common(2000))
# featuresets = [(document_features(d), c) for (d, c) in documents]
# train_set, test_set = featuresets[:12000], featuresets[12000:]

# trains data and prints accuracy

LinearSVC_classifier = SklearnClassifier(LinearSVC())
LinearSVC_classifier.train(train_set)
print("LinearSVC_classifier accuracy:", (nltk.classify.accuracy(LinearSVC_classifier, test_set)))

def append_truth_predictor(testSetSave, classifier):
    positives = [item for item in testSetSave if item[1][1] == 1]
    negatives = [item for item in testSetSave if item[1][1] == 0]
    print("Positives: " + str(len(positives)))
    print("Negatives: " + str(len(negatives)))

    toprint = []
    for thingy in testSetSave:
        title = thingy[0]
        d_f = thingy[1][0]
        relevance = thingy[1][1]
        # title = thingy[0]
        # cleaned = clean(title)
        # d_f = document_features(cleaned)
        # featurized = {}
        # for feature in d_f:
        #     if d_f[feature] == True:
        #         featurized[feature] = True
        thingy.append(classifier.classify(d_f))
        if np.asscalar(relevance) != np.asscalar(thingy[2]):
            toprint.append(thingy)
    for item in toprint:
        print(item[0] + ': ' + str(item[1][1]) + ' ' + str(item[2]))

    false_negatives = [item for item in toprint if item[1][1] == 1]
    print("Number of False_negatives is: " + str(len(false_negatives)))
    print("Number of False_positives is: " + str(len(toprint) - len(false_negatives)))

append_truth_predictor(test_set_save, LinearSVC_classifier)

# for loading in data
pickle.dump(LinearSVC_classifier, lsvc)
pickle.dump(word_features, wf)
pickle.dump(train_set_save_final, tr)
pickle.dump(test_set_save_final, te)

lsvc.close()
wf.close()
tr.close()
te.close()