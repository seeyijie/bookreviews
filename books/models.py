from application import db
from datetime import datetime


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    asin = db.Column(db.VARCHAR(255),nullable=False)
    helpful = db.Column(db.VARCHAR(100))
    overall = db.Column(db.Integer)
    dock_count = db.Column(db.SmallInteger)
    review_text = db.Column(db.VARCHAR(255))
    review_time = db.Column(db.Date)
    reviewer_id = db.Column(db.VARCHAR(100))
    reviewer_name = db.Column(db.VARCHAR(100))
    summary = db.Column(db.VARCHAR(255))


    def __init__(self, id, asin):
        self.id = id
        self.asin= asin


    def __repr__(self):
        return f'<Review {self.id}>'
