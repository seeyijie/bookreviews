from flask import Blueprint, render_template, redirect, session, url_for, request, jsonify
from werkzeug.security import generate_password_hash
from books.data_service import get_first_10_books
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


@book_app.route('/browse', methods=['GET'])
def get_meta_data():
    first_10_books = get_first_10_books()
    books =[]
    for book in first_10_books:
        books.append(book.serialize())
    return render_template('browse.html', arrayOfBooks= books)

# @book_app.route('/searchbyasin', methods=['GET'])
# def get_meta_data():
#     first_10_books = get_first_10_books()
#     books =[]
#     for book in first_10_books:
#         books.append(book.serialize())
#     return render_template('browse.html', arrayOfBooks= books)


