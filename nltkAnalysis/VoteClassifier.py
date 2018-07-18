from nltk.classify import ClassifierI
from statistics import mode

new_words = [('grab bike', 100), ('grab car', 100), ('grab pay', 100), ('grab app', 100), ('grab express', 100),
             ('surge pricing', 100), ('grab driver', 100), ('grab mod', 100), ('grab food', 100), ('mod grab', 100),
             ('grab ph', 100), ('grab indonesia', 100),
             ('grab phillipines', 100), ('anthony tan', 100), ('tan hooi ling', 100), ('grabmod', 100), ('grabpay', 100)]

new_words_list = []
for item in new_words:
    new_words_list.append(item[0])

def dehypdeslash(title):
    result1 = title
    if '-' in result1:
        result1 = title.split('-')
        result1 = ' '.join(result1)
    if '/' in result1:
        result1 = result1.split('/')
        result1 = ' '.join(result1)
    return result1

def is_special(features):
    for key in list(features.keys()):
        if key in new_words_list:
            special = True
        else:
            special = False
    return special

#put in classifiers as classifier, LogisticRegression, SGD_classifier

class VoteClassifier(ClassifierI):
    def __init__(self, *classifiers):
        self._classifiers = classifiers

    def old_classify(self, features):
        votes = []
        for c in self._classifiers:
            v = c.classify(features)
            votes.append(v)
        return mode(votes)

    def confidence(self, features):
        votes = []
        for c in self._classifiers:
            v = c.classify(features)
            votes.append(v)
        choice_votes = votes.count(mode(votes))
        conf = choice_votes / len(votes)
        return conf

    def classify(self, features):
        special = is_special(features)
        if special:
            print('ding ding ding')
            v = self._classifiers[2].classify(features)
        else:
            v1 = self._classifiers[0].classify(features)
            v2 = self._classifiers[1].classify(features)
            v3 = self._classifiers[2].classify(features)
            result = [v1, v2, v3]
            if result == [1,1,1]:
                v = 1
            elif result == [1,1,0]:
                v = 1
            elif result == [1,0,0]:
                v = 0
            elif result == [0,1,1]:
                v = 1
            elif result == [0,1,0]:
                v = 0
            elif result == [0,0,1]:
                v = 0
            elif result == [1,0,1]:
                v = 1
            elif result == [0,0,0]:
                v = 0
        return v





