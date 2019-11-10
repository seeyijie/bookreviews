from application import db


class Title(db.Model):
    asin = db.Column(db.VARCHAR(255), primary_key=True)
    title = db.Column(db.VARCHAR(255), nullable=True)
    def __init__(self, asin, title):
        self.asin = asin
        self.title = title
    def __repr__(self):
        return f'<AsinTitle {self.asin}>'
    def serialize(self):
        return {
            'title':self.title,
            'asin': self.asin
        }