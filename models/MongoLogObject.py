import mongoengine


class MongoLogObject(mongoengine.Document):
    timestamp = mongoengine.DateTimeField(required = True)
    method = mongoengine.StringField(required= True)
    url = mongoengine.StringField(required= True)
    response = mongoengine.StringField(required= True)
    meta = {
        'db_alias': 'core',
        'collection': 'logs'
    }
    def serialize(self):
        return {
            'timestamp': self.timestamp,
            'method': self.method,
            'url': self.url,
            'response': self.response
        }