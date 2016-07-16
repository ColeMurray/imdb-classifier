import pickle
import sqlite3

import os
from flask import Flask, render_template, request
from update import update_model
from vectorizer import vect
from wtforms import Form, TextAreaField, validators

### Preparing Classifier ###
cur_dir = os.path.dirname(__file__)
clf = pickle.load(open(os.path.join(cur_dir,
                                    'pkl_objects/classifier.pkl'), 'rb'))
db = os.path.join(cur_dir, 'reviews.sqlite')

update_model(db_path=db, model=clf, batch_size=10000)


# Uncomment the following lines if you are sure that
# you want to update your classifier.pkl file
# permanently.
# pickle.dump(clf, open(os.path.join(cur_dir,
# 'pkl_objects', 'classifier.pkl'), 'wb')
# , protocol=4)

def classify(document):
    label = {0: 'negative', 1: 'positive'}
    X = vect.transform([document])
    y = clf.predict(X)[0]
    proba = clf.predict_proba(X).max()
    return label[y], proba


def train(document, y):
    X = vect.transform([document])
    clf.partial_fit(X, [y])


def sqlite_entry(path, document, y):
    conn = sqlite3.connect(path)
    c = conn.cursor()
    c.execute("INSERT INTO review_db (review,sentiment, date) "
              " VALUES (?,?, DATETIME('now'))", (document, y))
    conn.commit()
    conn.close()


app = Flask(__name__)


class ReviewForm(Form):
    moviereview = TextAreaField('',
                                [validators.DataRequired(),
                                 validators.length(min=15)])


@app.route('/')
def index():
    form = ReviewForm(request.form)
    return render_template('reviewform.html', form=form)


@app.route('/results', methods=['POST'])
def results():
    form = ReviewForm(request.form)
    if request.method == 'POST' and form.validate():
        review = request.form['moviereview']
        y, proba = classify(review)
        return render_template('results.html',
                               content=review,
                               prediction=y,
                               probability=round(proba * 100, 2))
    else:
        return render_template('reviewform.html', form=form)


@app.route('/thanks', methods=['POST'])
def feedback():
    feedback = request.form['feedback_button']
    review = request.form['review']
    prediction = request.form['prediction']
    inv_label = {'negative': 0, 'positive': 1}
    y = inv_label[prediction]
    if feedback == 'Incorrect':
        y = int(not (y))
    train(review, y)
    sqlite_entry(db, review, y)
    return render_template('thanks.html')


if __name__ == '__main__':
    clf = update_model(db_path=db, model=clf, batch_size=10000)
    app.run(debug=True)