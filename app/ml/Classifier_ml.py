from collections import defaultdict
import pickle
import numpy as np
import nltk


with open("ml/classifier.pkl", "rb") as f:
    clf = pickle.load(f)
with open("ml/dict_of_words.pkl", "rb") as f:
    dict_of_words = pickle.load(f)
with open("ml/enum_keys.pkl", "rb") as f:
    enum_keys = pickle.load(f)
estimator = clf

def split_and_filter(comment):
    tokens = nltk.word_tokenize(comment)
    tagged = nltk.pos_tag(tokens)
    tagged = np.array(tagged).T
    filtered = []
    filt = ['JJ', 'NN']
    for f in filt:
        filtered.append(tagged[0, np.where(tagged[1] == f)])
    lemmatizer = nltk.stem.wordnet.WordNetLemmatizer()
    lemmatized = [[lemmatizer.lemmatize(x) for x in filtered[i][0]] for i in range(2)]
    return lemmatized


# Предсказатель
def predict(comment):
    X = np.zeros((1, len(dict_of_words)+1))
    lt = split_and_filter(comment)
    for i in range(2):
        for w in lt[i]:
            if dict_of_words.get(w):
                X[0][dict_of_words[w]] += 1
    return enum_keys[estimator.predict(X)[0]][1]

def text_to_emojis(reviews):
    texts = [r.text for r in reviews]
    freqs = {}
    for comment in texts:
        pred = predict(comment)
        freqs[pred] = freqs.get(pred, 0) + 1
    return list(freqs.items())

