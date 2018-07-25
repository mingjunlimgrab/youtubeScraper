from nltk.classify import ClassifierI
from statistics import mode

new_words = [('grab app', 100), ('grab mod', 100), ('mod grab', 100), ('grabmod', 100)]

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
    special = False
    for key in list(features.keys()):
        for word in new_words_list:
            word = 'contains' + '(' + word + ')'
            if features[word] == True:
                special = True
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
            v = self._classifiers[2].classify(features)
        else:
            v1 = self._classifiers[0].classify(features)
            v2 = self._classifiers[1].classify(features)
            v3 = self._classifiers[2].classify(features)
            result = [v1, v2, v3]
            if result == ['HIG', 'HIG', 'HIG']:
                v = 'HIG'
            elif result == ['HIG', 'HIG', 'LOW']:
                v = 'HIG'
            elif result == ['HIG', 'LOW', 'LOW']:
                v = 'LOW'
            elif result == ['LOW', 'HIG', 'HIG']:
                v = 'HIG'
            elif result == ['LOW', 'HIG', 'LOW']:
                v = 'LOW'
            elif result == ['LOW', 'LOW', 'HIG']:
                v = 'LOW'
            elif result == ['HIG', 'LOW', 'HIG']:
                v = 'HIG'
            elif result == ['LOW', 'LOW', 'LOW']:
                v = 'LOW'
            else:
                v = 'LOW'
                print('Something went wrong')
        return v


