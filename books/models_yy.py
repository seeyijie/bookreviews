from application import db
from datetime import date

#corresponds to last entry from kaggle dataset

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    asin = db.Column(db.VARCHAR(255),nullable=False)
    helpful = db.Column(db.VARCHAR(100))
    overall = db.Column(db.Integer)
    reviewText = db.Column(db.VARCHAR(255))
    reviewTime = db.Column(db.Date)
    reviewerID = db.Column(db.VARCHAR(100))
    reviewerName = db.Column(db.VARCHAR(100))
    summary = db.Column(db.VARCHAR(255))
    unixReviewTime = db.Column(db.Integer) 


    #init only with summary and asin for testing
    def __init__(self, asin, summary):
        self.asin= asin
        now = date.today()
        formated = now.strftime("%m %-d, %Y")
        self.reviewTime = formated
        self.summary = summary
        

    def __repr__(self):
        return f'<Review {self.id}>'
