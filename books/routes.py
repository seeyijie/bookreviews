from flask import Blueprint, render_template, redirect, session, url_for, request, jsonify
from werkzeug.security import generate_password_hash

from application import db
from books.models import Reviews

book_app = Blueprint('book_app', __name__)

@book_app.route('/book/<asin>/reviews', methods=['GET'])
def get_reviews(asin):
    results = Reviews.query.filter_by(asin=asin)
    reviews = []
    for result in results:
        reviews.append(result.serialize())
    return jsonify(reviews)
    #return render_template('book.html', reviews=reviews)
