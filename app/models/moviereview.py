from app import db


# class MovieReview:
#     def __init__(self, path, document, y):
#         conn = sqlite3.connect(path)
#         c = conn.cursor()
#         c.execute("INSERT INTO review_db (review,sentiment, date) "
#                   " VALUES (?,?, DATETIME('now'))", (document, y))
#         conn.commit()
#         conn.close()


class Base(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())


class Review(Base):
    __tablename__ = 'review'

    review = db.Column(db.String)
    sentiment = db.Column(db.Integer)

    def __init__(self, review, sentiment):
        self.review = review
        self.sentiment = sentiment
