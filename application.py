from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

import time
from logging.config import fileConfig   # for logging
from models.logs import LoggerObject    # for logging
import threading                        # to create a thread for logging
# NOTE
# with logging being recorded, there will no longer be log messages shown in the console.
# these log messages can be found in /models/bookreviews.log.

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config.from_pyfile('settings.py')

    db.init_app(app)
    migrate = Migrate(app, db)

    from users.routes import user_app
    from books.routes import book_app
    from models.routes import server_log

    app.register_blueprint(user_app)
    app.register_blueprint(book_app)
    app.register_blueprint(server_log)

    return app

# thread class for logging while server is up
class logThread(threading.Thread):
    def __init__(self, threadID):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.logger = LoggerObject()    # creates a loggerobject defined in logs.py
    
    def run(self):
        self.logger.clearlogtxt()            # clear text in bookreviews.log
        self.logger.deleteAllLogs()          # clear all logs in mongoDB
        while True:
            self.logger.log()
            print('snapshot logged: ', self.logger.getLogCount())       # comment me out in production
            # print (self.logger.getAllLogs())                          # comment me out in production as well
            time.sleep(5)                                               # updates log every 5 seconds
            
fileConfig('models/logging.cfg')                    # sets up log
logging_thread = logThread(1)                       # defines a thread that transfers info from bookreviews.log into mongoDB
logging_thread.start()                              # starts the thread