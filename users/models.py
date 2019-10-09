from application import db
from datetime import datetime


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.VARCHAR(100))
    email = db.Column(db.VARCHAR(100))
    password = db.Column(db.VARCHAR(100))
    recent_login = db.Column(db.DateTime)

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password
        now = datetime.now()
        formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
        self.recent_login = formatted_date

    def __repr__(self):
        return f'<User {self.user}>'
