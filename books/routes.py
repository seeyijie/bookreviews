from flask import Blueprint, render_template, redirect, session, url_for, request, jsonify
from werkzeug.security import generate_password_hash
from books.data_service import get_first_10_books
from application import db
from books.models import Review

book_app = Blueprint('book_app', __name__)

@book_app.route('/book/<asin>/reviews', methods=['GET'])
def get_reviews(asin):
    results = Review.query.filter_by(asin=asin)
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


#query book review
@book_app.route('/books/', methods=['GET', 'POST'])
def get_reviewss():
    reviews = []
    search = False
    if request.args:
        search = True
        asin = request.args['asin']
        reviews = Review.query.filter_by(asin=asin).all()
    else:
        reviews = Review.query.limit(20).all()

    return render_template('books_test.html', reviews=reviews, search=search)

#add a book review
@book_app.route('/add/', methods=['GET','POST'])
def add_review():
    if request.method == 'POST':
        asin = request.form['asin']
        summary = request.form['summary']
        print(request.form['summary'])
        print(summary)
        review = Review(asin, summary)
        db.session.add(review)
        db.session.commit()
        print(f'review_id: {review.id}')
        return f'review_id: {review.id}'


    return render_template('add_review_test.html')

