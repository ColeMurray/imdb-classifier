# coding: utf-8
import os
import pickle

from vectorizer import vect

clf = pickle.load(open(os.path.join('pkl_objects', 'classifier.pkl'), 'rb'))
import numpy as np

label = {0: 'negative', 1: 'positive'}
X = vect.transform(['Great film, well done.'])
print('Prediction %s\n Probability: %.2f%%' % (label[clf.predict(X)[0]],
                                               np.max(clf.predict_proba(X)) * 100))
