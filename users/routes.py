from flask import Blueprint, request, jsonify
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required,
                                jwt_refresh_token_required, get_jwt_identity)
from users.user_schema import validate_user

from werkzeug.security import generate_password_hash, check_password_hash

from application import db
from users.models import User
from users.forms import RegisterForm, LoginForm
from scrape import Scraper, load_list
import time
from models.logs import LoggerObject
import os

logger = LoggerObject()

user_app = Blueprint('user_app', __name__)


# Temporarily put in user app to upload data to MySQL
# @user_app.route('/scrape', methods=['GET'])
# def scrape():
#     start = time.time()
#     scraper = Scraper()
#     upper_limit = int(request.args.get('upper_limit'))
#     lower_limit = int(request.args.get('lower_limit'))
#     print("ASIN Review IDs Path: " + os.path.join(user_app.root_path, "../misc/reviews_asin.csv"))
#     asin_list = load_list(os.path.join(user_app.root_path, "../misc/reviews_asin.csv"))
#     print(len(asin_list))
#     url_list = scraper.create_URL(asin_list)
#     res_list = scraper.get_response(url_list, upper_limit=upper_limit, lower_limit=lower_limit)
#     scraper.scrape(res_list, asin_list, fileout="/home/yijie/Desktop/title_to_asin_2.csv",
#                    err_logs="/home/yijie/Desktop/errs_logs.txt")

#     elapsed_time = time.time() - start
#     print("Duration: {}".format(elapsed_time))
#     return "Success"


@user_app.route('/register', methods=['POST'])
def register():
    data = validate_user(request.get_json())
    if data['ok']:
        data = data['data']
        hashed_password = generate_password_hash(data['password'])  # Salt + SHA256
        user = User(
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
        res.status_code = 400
        logger.logrequest(request, res)
        return res


@user_app.route('/login', methods=['POST'])
def auth_user():
    data = validate_user(request.get_json())
    if data['ok']:
        data = data['data']
        user = User.query.filter_by(email=data['email']).first()
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
            res.status_code = 200
            logger.logrequest(request, res)
            return res
        else:
            res = jsonify({'ok': False, 'message': 'Invalid username or password'})
            res.status_code = 401
            logger.logrequest(request, res)
            return res
    else:
        res = jsonify({'ok': False, 'message': 'Bad request parameters: {}'
                       .format(data['message'])})
        res.status_code = 400
        return res


# @user_app.route('/refresh', methods=['POST'])
# @jwt_refresh_token_required
# def refresh():
#     current_user = get_jwt_identity()
#     access_token = create_access_token(identity=current_user)
#     return {'access_token': access_token}


# @user_app.route('/hello', methods=['GET'])
# # protect routes
# @jwt_required
# def hello():
#     return jsonify({'data': 'Hello world'}), 200