from application import db
import string
from random import randint

class User(db.Model):
    id = db.Column(db.VARCHAR(100), nullable=False)  # Starts with B
    name = db.Column(db.VARCHAR(100), nullable=False)
    email = db.Column(db.VARCHAR(100), primary_key=True)
    password = db.Column(db.VARCHAR(100), nullable=False)

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password
        self.id = "B"
        for i in range(13):
            self.id += string.printable[randint(0, 36)].upper()

    def __repr__(self):
        return f'<User {self.user}>'
