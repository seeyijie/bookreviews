import os

FLASK_APP = "manage.py"
FLASK_ENV = "development"
MYSQL_HOST = "localhost"
MYSQL_PORT = 3306
DBNAME = "50043_DB"
SECRET_KEY = os.environ.get("SECRET_KEY", default="secret")
MYSQL_USERNAME = os.environ.get("MYSQL_USER", default="root")
MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD", default="password")
MYSQL_URI = "mysql+pymysql://%s:%s@%s:3306/%s" % (MYSQL_USERNAME, MYSQL_PASSWORD, MYSQL_HOST, DBNAME)
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = MYSQL_URI