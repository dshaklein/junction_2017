import pickle
import operator
import nltk
import numpy as np

# dict_synonyms
with open("extended_categories.json", "rb") as f:
    dict_main = pickle.load(f)
    print(dict_main.keys())

def split_and_filter(comment):
    tokens = nltk.word_tokenize(comment)
    tagged = nltk.pos_tag(tokens)
    tagged = np.array(tagged).T
    filtered = []
    filt = ['JJ', 'NN']
    for f in filt:
        filtered.append(tagged[0, np.where(tagged[1] == f)])
    lemmatizer = nltk.stem.wordnet.WordNetLemmatizer()
    result = []
    for i in range(len(filt)):
        result.extend([lemmatizer.lemmatize(x) for x in filtered[i][0]])
    return result


# веса главных слов и синонимов
def text_to_emoji(reviews):
    texts = [r.text for r in reviews]
    text = ' '.join(texts)
    emojis = dict.fromkeys(dict_main.keys(), 0)
    ltxt = split_and_filter(text)
    for word in ltxt:
        for key in emojis.keys():
            if word in dict_main[key]:
                emojis[key] += 1
    return sorted(emojis.items(), key=operator.itemgetter(1))
