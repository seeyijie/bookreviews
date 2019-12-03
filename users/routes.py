from flask import Blueprint, request, jsonify
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity)
from users.user_schema import validate_user
from werkzeug.security import generate_password_hash, check_password_hash

from application import db
from users.models import Users
from users.forms import RegisterForm, LoginForm
from scrape import Scraper, load_list
import time
from models.logs import LoggerObject
import os

logger = LoggerObject()

user_app = Blueprint('user_app', __name__)

@user_app.route('/register', methods=['POST'])
def register():
    data = validate_user(request.get_json())
    if data['ok']:
        data = data['data']
        hashed_password = generate_password_hash(data['password'])  # Salt + SHA256
        user = Users(
            data['name'],
            data['email'],
            hashed_password
        )
        db.session.add(user)
        db.session.commit()
        res = jsonify({'ok': True, 'message': 'User created successfully!'}), 200
        res[0].status_code = 200
        logger.logrequest(request, res[0])
        return res
    else:
        res = jsonify({'ok': False, 'message': 'Bad request parameters: {}'
                       .format(data['message'])})
        res[0].status_code = 400
        logger.logrequest(request, res)
        return res

@user_app.route('/login', methods=['POST'])
def auth_user():
    data = validate_user(request.get_json())
    if data['ok']:
        data = data['data']
        user = Users.query.filter_by(email=data['email']).first()
        if user and check_password_hash(user.password, data['password']):
            access_token = create_access_token(identity=data)
            refresh_token = create_refresh_token(identity=data)
            token = {
                'name': user.name,
                'id': user.id,
                'access_token': access_token,
                'refresh_token': refresh_token
            }
            res = jsonify({'ok': True, 'data': token}), 200
            res[0].status_code = 200
            logger.logrequest(request, res)
            return res
        else:
            res = jsonify({'ok': False, 'message': 'Invalid username or password'})
            res[0].status_code = 401
            logger.logrequest(request, res)
            return res
    else:
        res = jsonify({'ok': False, 'message': 'Bad request parameters: {}'
                       .format(data['message'])})
        res[0].status_code = 400
        return res