from nltk.tokenize import word_tokenize
import pickle
import random
import pandas as pd
import VoteClassifierThreat as vc
import nltk

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

new_words = [('grab mod', 100), ('mod grab', 100), ('grabmod', 100)]

deterministic = [' grab mod ', ' mod grab ', 'mod grab ', 'grabmod']

c = open('my_classifier_threat.pickle', 'rb')
mnb = open('MNB_classifier_threat.pickle', 'rb')
bnb = open('BernoulliNB_classifier_threat.pickle', 'rb')
lg = open('LogisticRegression_classifier_threat.pickle', 'rb')
sgd = open('SGD_classifier_threat.pickle', 'rb')
lsvc = open('LinearSVC_classifier_threat.pickle', 'rb')
wf = open('word_features_threat.pickle', 'rb')
tr = open('train_set_threat.pickle', 'rb')
te = open('test_set_threat.pickle', 'rb')

classifier = pickle.load(c)
MNB_classifier = pickle.load(mnb)
BernoulliNB_classifier = pickle.load(bnb)
LogisticRegression = pickle.load(lg)
SGD_classifier = pickle.load(sgd)
LinearSVC_classifier = pickle.load(lsvc)
word_features = pickle.load(wf)
train_set = pickle.load(tr)
test_set = pickle.load(te)

vote_classifier = vc.VoteClassifier(classifier, LogisticRegression, SGD_classifier)

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

def predictor(titles):
    for title in titles:
        cleaned = clean(title)
        d_f = document_features(cleaned)
        print(title + ': ' + str(vote_classifier.classify(d_f)))

def truth_predictor(titles):
    for title in titles:
        cleaned = clean(title)
        d_f = document_features(cleaned)
        featurized = {}
        for feature in d_f:
            if d_f[feature] == True:
                featurized[feature] = True
        print(title + ': ' + str(vote_classifier.classify(featurized)))

def special_features(title):
    toke = []
    for item in new_words:
        if item[0] in title.lower():
            toke.append(item[0])
    return toke

# Takes in a list of lists [[Title, relevance], [Title, relevance], ...] and appends true classification to the end of each list
def append_truth_predictor(titlesWithRelevance, classifier):
    high = [item for item in titlesWithRelevance if item[1] == 'HIG']
    low = [item for item in titlesWithRelevance if item[1] == 'LOW']
    print("high: " + str(len(high)))
    print("low: " + str(len(low)))

    toprint = []
    for thingy in titlesWithRelevance:
        title = thingy[0]
        title = dehypdeslash(title)
        toke = special_features(title)
        cleaned = clean(title)
        for item in toke:
            cleaned.append(item)
        d_f = document_features(cleaned)
        # featurized = {}
        # for feature in d_f:
        #     if d_f[feature] == True:
        #         featurized[feature] = True
        if len(thingy) == 3:
            thingy[2] = classifier.classify(d_f)
        else:
            thingy.append(classifier.classify(d_f))
        if thingy[1] != thingy[2]:
            toprint.append(thingy)
    for item in toprint:
        print(item[0] + ': ' + str(item[1]) + ' ' + str(item[2]))

    false_negatives = [item for item in toprint if item[1] == 'HIG']
    print("Number of False_negatives is: " + str(len(false_negatives)))
    print("Number of False_positives is: " + str(len(toprint) - len(false_negatives)))

def positive_append(titlesWithRelevance, classifier, printt=False):
    # print(titlesWithRelevance)
    positives = [item for item in titlesWithRelevance if item[1] == 1]
    print("Positives: " + str(len(positives)))

    toprint = []
    for thingy in positives:
        title = thingy[0]
        title = dehypdeslash(title)
        toke = special_features(title)
        cleaned = clean(title)
        for item in toke:
            cleaned.append(item)
        d_f = document_features(cleaned)
        if len(thingy) == 3:
            thingy[2] = classifier.classify(d_f)
        else:
            thingy.append(classifier.classify(d_f))
        if int(thingy[1]) != int(thingy[2]):
            toprint.append(thingy)
    if printt:
        for item in toprint:
            print(item[0] + ': ' + str(item[1]) + ' ' + str(item[2]))

    false_negatives = [item for item in toprint if item[1] == 'HIG']
    print("Number of False_negatives is: " + str(len(false_negatives)))

def checker(title):
    for word in deterministic:
        if word in title:
            return True
    return False

def LinearSVC_deterministic_predictor(titlesWithRelevance, classifier):
    high = [item for item in titlesWithRelevance if item[1] == 'HIG']
    low = [item for item in titlesWithRelevance if item[1] == 'LOW']
    print("High: " + str(len(high)))
    print("Low: " + str(len(low)))

    toprint = []

    for thingy in titlesWithRelevance:
        title = thingy[0]
        title = dehypdeslash(title)
        if checker(title.lower()):
            if len(thingy) == 3:
                thingy[2] = 'HIG'
            else:
                thingy.append('HIG')
            continue

        toke = special_features(title)
        cleaned = clean(title)
        for item in toke:
            cleaned.append(item)
        d_f = document_features(cleaned)
        if len(thingy) == 3:
            thingy[2] = classifier.classify(d_f)
        else:
            thingy.append(classifier.classify(d_f))

        if thingy[1] != thingy[2]:
            toprint.append(thingy)

    for item in toprint:
        print(item[0] + ': ' + str(item[1]) + ' ' + str(item[2]))

    false_negatives = [item for item in toprint if item[1] == 'HIG']
    print("Number of False_negatives is: " + str(len(false_negatives)))
    print("Number of False_positives is: " + str(len(toprint) - len(false_negatives)))

def create_test_set(csvFileName): #takes in a string (the name of a file or directory)
    df = pd.read_csv(csvFileName)
    documents = []
    lib = []
    index = 0
    for title in df['title']:
        documents.append([title, df['threat'][index]])
        index += 1
    test_set = documents
    return test_set

documents = []
index = 0
for thingy in test_set:
    title = thingy[0]
    title = dehypdeslash(title)
    toke = special_features(title)
    cleaned = clean(title)
    for item in toke:
        cleaned.append(item)
    d_f = document_features(cleaned)
    documents.append((d_f, thingy[1]))
    index += 1

predicting_titles = ['Man has 156 seconds to grab free stuff', 'How to collect a Grab Sample', 'what happens when i grab my dog\'s tail',
                     'How to grab coupons', 'Grab Mod 3.2', 'What it\'s like to be a Grabcar Driver', 'Grab driver mod 5.31.4',
                     'grab premium kuala lumpur', 'Uber Agrees to Sell Southeast Asian Operations to Rival Grab',
                     'grab gps tutorial', 'grab driver tutorial', 'spotlight: grab dos & don\'ts', 'grabtaxi new driver training video',
                     '[SOCIAL EXPERIMENT] GOJEK vs. GRAB vs. UBER', 'grab thailand', 'anthony tan from grabtaxi', 'grab co-founder tan hooi ling',
                     'ride hailing company grab', 'no auto food grab mod']

test_set = create_test_set('/Users/mingjun.lim/Documents/youtubeScraper/Data/firstRound.csv')
# print("Original Naive Bayes accuracy:", (nltk.classify.accuracy(classifier, documents)))
# append_truth_predictor(test_set, classifier)
# print("MNB_classifier accuracy:", (nltk.classify.accuracy(MNB_classifier, documents)))
# append_truth_predictor(test_set, MNB_classifier)
# print("BernoulliNB_classifier accuracy:", (nltk.classify.accuracy(BernoulliNB_classifier, documents)))
# append_truth_predictor(test_set, BernoulliNB_classifier)
# print("LogisticRegression_classifier accuracy:", (nltk.classify.accuracy(LogisticRegression, documents)))
# append_truth_predictor(test_set, LogisticRegression)
# print("SGD_classifier accuracy:", (nltk.classify.accuracy(SGD_classifier, documents)))
# append_truth_predictor(test_set, SGD_classifier)
# print("LinearSVC_classifier accuracy:", (nltk.classify.accuracy(LinearSVC_classifier, documents)))
# append_truth_predictor(test_set, LinearSVC_classifier)
# print("voteclassifier accuracy:", (nltk.classify.accuracy(vote_classifier, documents)))
# append_truth_predictor(test_set, vote_classifier)
append_truth_predictor(test_set, vote_classifier)

test_set = create_test_set('firstRoundSorted.csv')
print("Original Naive Bayes accuracy:", (nltk.classify.accuracy(classifier, documents)))
append_truth_predictor(test_set, classifier)
# positive_append(test_set, classifier, True)
print("MNB_classifier accuracy:", (nltk.classify.accuracy(MNB_classifier, documents)))
append_truth_predictor(test_set, MNB_classifier)
# positive_append(test_set, MNB_classifier, False)
print("BernoulliNB_classifier accuracy:", (nltk.classify.accuracy(BernoulliNB_classifier, documents)))
append_truth_predictor(test_set, BernoulliNB_classifier)
# positive_append(test_set, BernoulliNB_classifier, False)
print("LogisticRegression_classifier accuracy:", (nltk.classify.accuracy(LogisticRegression, documents)))
append_truth_predictor(test_set, LogisticRegression)
# positive_append(test_set, LogisticRegression, True)
print("SGD_classifier accuracy:", (nltk.classify.accuracy(SGD_classifier, documents)))
append_truth_predictor(test_set, SGD_classifier)
# positive_append(test_set, SGD_classifier, True)
print("LinearSVC_classifier accuracy:", (nltk.classify.accuracy(LinearSVC_classifier, documents)))
append_truth_predictor(test_set, LinearSVC_classifier)
# positive_append(test_set, LinearSVC_classifier, True)
# print("voteclassifier accuracy:", (nltk.classify.accuracy(vote_classifier, documents)))
# append_truth_predictor(test_set, vote_classifier)
# positive_append(test_set, vote_classifier, True)
LinearSVC_deterministic_predictor(test_set, LinearSVC_classifier)

c.close()
mnb.close()
bnb.close()
lg.close()
sgd.close()
lsvc.close()
wf.close()
tr.close()
te.close()