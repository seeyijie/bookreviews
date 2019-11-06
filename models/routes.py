from flask import Blueprint, render_template, redirect, session, url_for, request, jsonify
from werkzeug.security import generate_password_hash
from models.logs import LoggerObject
# from application import db

logger = LoggerObject()

server_log = Blueprint('server_log', __name__)

@server_log.route('/log', methods=['GET'])
def get_log():
    # obtain log from mongoDB
    logger2 = LoggerObject()
    logger.logrequest(request, 'displayed on this page')
    return render_template('log.html', loglist = logger2.getAllLogs())

@server_log.route('/deletelogs', methods=['GET'])
def delete_log():
    logger.deleteAllLogs()
    return "cleared all logs"
