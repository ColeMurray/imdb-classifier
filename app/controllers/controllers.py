from app import app
from app import db
from app.classifier import train, classify
from app.models.moviereview import Review
from app.views.forms import ReviewForm
from flask import render_template, request


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

    reviewModel = Review(review=review, sentiment=y)
    db.session.add(reviewModel)
    db.session.commit()
    # sqlite_entry(db, review, y)
    return render_template('thanks.html')
