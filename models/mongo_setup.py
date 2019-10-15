import mongoengine
alias = 'core'
db = '50043_db'

def global_init():
    mongoengine.register_connection(alias='core', name = db , host='3.16.15.52', port = 27017,username='root', password='password',db = db)