from application import db
from datetime import datetime


class Reviews(db.Model):
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
    def __init__(self, asin, summary, reviewText, reviewerID, reviewerName):
        self.asin = asin
        self.summary = summary
        self.reviewerID = reviewerID
        self.reviewerName = reviewerName
        self.helpful = "[0, 0]"
        self.overall = 0
        now = datetime.now()
        self.reviewTime = now.strftime("%Y-%-m-%-d")
        self.reviewText = reviewText
        self.unixReviewTime = int(now.timestamp())

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


