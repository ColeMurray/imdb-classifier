# vectorizer.py
import os
import pickle
import re

from sklearn.feature_extraction.text import HashingVectorizer

cur_dir = os.path.dirname(__file__)
stop = pickle.load(open(
    os.path.join(cur_dir,
                 'pkl_objects',
                 'stopwords.pkl'), 'rb'))

"""
Remove all html tags. Replace any emoticons. Remove all stop words

"""


def tokenizer(text):
    text = re.sub('<[^>]*>', '', text)
    emoticons = re.findall('(?::|;|=) (?:-)?(?:\) |\(|D|P)', text)
    text = re.sub('[\W]+', ' ', text.lower()) + ' '.join(emoticons).replace('-', '')
    tokenized = [w for w in text.split() if w not in stop]
    return tokenized


vect = HashingVectorizer(decode_error='ignore',
                         n_features=2 ** 21,
                         preprocessor=None,
                         tokenizer=tokenizer)
