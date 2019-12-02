
import mongoengine
alias = 'core'
db = '50043_db'

# this IP is transferred over to the server after status check
f = open("/home/ubuntu/config_flask_ip.txt","r")
mongodb_ip = f.read()

# old ip address: 3.16.15.52
def global_init():
    mongoengine.register_connection(alias='core', name = db , host=mongodb_ip, port = 27017,username='root', password='password',db = db)
    # mongoengine.register_connection(alias='core', name = db ) #commented top one out to connect to localhost