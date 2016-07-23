import numpy as np

from app.models.moviereview import Review
from app.vectorizer import vect


def update_model(model, batch_size=10000):
    offset = 0
    results = Review.query.with_entities(Review.review, Review.sentiment).limit(batch_size).all()
    while results:
        offset += batch_size
        data = np.array(results)
        X = data[:, 0]
        y = data[:, 1].astype(int)
        classes = np.array([0, 1])
        X_train = vect.transform(X)
        model.partial_fit(X_train, y, classes=classes)
        results = Review.query.with_entities(Review.review, Review.sentiment).limit(batch_size).offset(offset).all()

    return model
