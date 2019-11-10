from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager
import time
import threading  # to create a thread for logging
import models.mongo_setup as mongo_setup

db = SQLAlchemy()



def create_app():
    app = Flask(__name__)
    mongo_setup.global_init()
    app.config.from_pyfile('settings.py')
    CORS(app)

    db.init_app(app)
    migrate = Migrate(app, db)
    jwt = JWTManager(app)

    from users.routes import user_app
    from books.routes import book_app
    from SearchBook.routes import search_app
    from models.routes import server_log

    app.register_blueprint(user_app)
    app.register_blueprint(book_app)
    app.register_blueprint(server_log)
    app.register_blueprint(search_app)

    return app
