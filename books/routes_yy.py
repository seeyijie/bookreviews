from flask import Blueprint, render_template, request

from application import db
from books.models import Review

book_app = Blueprint('book_app', __name__)

#query book review
@book_app.route('/books/', methods=['GET', 'POST'])
def get_reviews():
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

