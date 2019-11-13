from application import db
from datetime import date


class Review(db.Model):
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    asin = db.Column(db.VARCHAR(100))
    helpful = db.Column(db.VARCHAR(100))
    overall = db.Column(db.Integer)
    reviewText = db.Column(db.VARCHAR(255))
    reviewTime = db.Column(db.Date)
    reviewerID = db.Column(db.VARCHAR(100))
    reviewerName = db.Column(db.VARCHAR(100))
    summary = db.Column(db.VARCHAR(255))
    unixReviewTime = db.Column(db.Integer)

    # init only with summary and reviewText for now
    def __init__(self, asin, reviewText,reviewerName):
        self.asin = asin
        now = date.today()
        formated = now.strftime("%m %-d, %Y")
        self.reviewTime = formated
        self.reviewText = reviewText
        self.reviewerName = reviewerName

    def serialize(self):
        return {
            'id': self.id,
            'asin': self.asin,
            'helpful': self.helpful,
            'overall': self.overall,
            'reviewText': self.reviewText,
            'reviewTime': self.reviewTime,
            'reviewerID': self.reviewerID,
            'reviewerName': self.reviewerName,
            'summary': self.summary,
            'unixReviewTime': self.unixReviewTime
        }

    def __repr__(self):
        return f'<Review {self.id}>'


