import nltk
from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.naive_bayes import MultinomialNB,BernoulliNB
import pickle
from statistics import mode
from nltk.classify import ClassifierI
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.svm import SVC, LinearSVC, NuSVC


class VoteClassifier(ClassifierI):
    def __init__(self, *classifiers):
        self._classifiers = classifiers

    def classify(self, features):
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

##posts = nltk.corpus.nps_chat.xml_posts()[:10000]

def dialogue_act_features(post):
    features = {}
    for word in nltk.word_tokenize(post):
        features['contains({})'.format(word.lower())] = True
    return features
##
##featuresets = [(dialogue_act_features(post.text), post.get('class')) for post in posts]
##size = int(len(featuresets) * 0.1)
##train_set, test_set = featuresets[size:], featuresets[:size]
##
##print("***** Classification Starts *****")
##
##MNB_classifier = SklearnClassifier(MultinomialNB())
##MNB_classifier.train(train_set)
##
##BNB_classifier = SklearnClassifier(BernoulliNB())
##BNB_classifier.train(train_set)
##
##LogisticRegression_classifier = SklearnClassifier(LogisticRegression())
##LogisticRegression_classifier.train(train_set)
##
##SGDClassifier_classifier = SklearnClassifier(SGDClassifier())
##SGDClassifier_classifier.train(train_set)
##
##LinearSVC_classifier = SklearnClassifier(LinearSVC())
##LinearSVC_classifier.train(train_set)
##
####NuSVC_classifier = SklearnClassifier(NuSVC())
####NuSVC_classifier.train(train_set)
##
##voted_classifier = VoteClassifier(
##                            MNB_classifier, BNB_classifier,
##                            LogisticRegression_classifier, SGDClassifier_classifier,
##                            LinearSVC_classifier
##                            
##    )
##
##file = open('important.pickle', 'wb')
##pickle.dump(voted_classifier, file)
##file.close()
##

classifier_f = open("important.pickle", "rb")
voted_classifier = pickle.load(classifier_f)
classifier_f.close()

def response(text):
    feats = dialogue_act_features(text)
    return voted_classifier.classify(feats), voted_classifier.confidence(feats)
