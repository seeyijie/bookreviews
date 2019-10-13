import mongoengine
alias = 'core'
db = '50043_db'

def global_init():
    mongoengine.register_connection(alias='core', name = db )