from application import db
from datetime import date
import mongoengine

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

    #init only with summary and asin for testing
    def __init__(self, asin, summary):
        self.asin= asin
        now = date.today()
        formated = now.strftime("%m %-d, %Y")
        self.reviewTime = formated
        self.summary = summary
        


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

class BookMetaData(mongoengine.Document):
    asin = mongoengine.StringField(required=True)
    imUrl = mongoengine.StringField(required=True)
    related = mongoengine.DictField()
    categories = mongoengine.ListField(required=True)
    description = mongoengine.StringField(required=True)
    price = mongoengine.FloatField(required = False)

    meta = {
        'db_alias' : 'core',
        'collection': 'books_metadata'
    }
    def serialize(self):
        return {
            'asin': self.asin,
            'imUrl': self.imUrl
        }
