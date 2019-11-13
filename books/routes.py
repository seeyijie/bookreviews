from flask import Blueprint, render_template, redirect, session, url_for, request, jsonify
from werkzeug.security import generate_password_hash
from books.data_service import get_first_10_books
from books.data_service import get_book_by_asin
from books.data_service import deleteReview
from application import db
from books.models import Review
from models.logs import LoggerObject    # for logging
import json

book_app = Blueprint('book_app', __name__)
logger = LoggerObject()

'''
@book_app.route('/book/<asin>/reviews', methods=['GET'])
def get_reviews(asin):
    results = Review.query.filter_by(asin=asin)
    reviews = []
    for result in results:
        reviews.append(result.serialize())
    return jsonify(reviews)
    #return render_template('book.html', reviews=reviews)
'''

@book_app.route('/browse', methods=['GET'])
def get_meta_data():
    msg=''
    if request.args:
        msg= request.args['msg']

    first_10_books = get_first_10_books()
    books =[]
    for book in first_10_books:
        books.append(book.serialize())
    logger.logrequest(request)
    return render_template('browse.html', arrayOfBooks= books, msg=msg)

@book_app.route('/searchbyasin', methods=['GET'])
def get_byasin():
    first_10_books = get_book_by_asin('B0002IQ15S')
    books =[]
    for book in first_10_books:
        books.append(book.serialize())
    logger.logrequest(request)
    return render_template('browse.html', arrayOfBooks= books)


@book_app.route('/books/<asin>', methods=['GET', 'POST'])
def get_book(asin):
    # if a review is submitted
    if request.method == 'POST':
        asin = asin
        reviewText = request.form['reviewText']
        review = Review(asin, reviewText)
        db.session.add(review)
        db.session.commit()

    # query asin from mongo and mysql
    book = get_book_by_asin(asin)

    # if a book is found
    if (len(book) > 0):
        book = book[0]
        reviews = Review.query.filter_by(asin=asin).all()
        reviews = reviews[::-1] #sort by latest
        logger.logrequest(request)
        return render_template('book.html', reviews=reviews, book=book)
    else:
        err_msg = 'Book not found.'
        logger.logrequest(request)
        return redirect(url_for('.get_meta_data', msg=err_msg))

@book_app.route('/api/books/<asin>', methods=['GET', 'POST'])
def get_book_endpoint(asin):
    # query asin from mongo and mysql
    book = get_book_by_asin([asin])
    print(book[0].related)# this is a dictionary

    related_url = {}
    for key in book[0].related:
        related_url[key]=get_list_asin_details(book[0].related[key])
    # if a book is found
    if (len(book) > 0):
        book = book[0]
        reviews_raw = Review.query.filter_by(asin=asin).all()
        reviews_raw = reviews_raw[::-1] #sort by latest
        reviews = []
        for review in reviews_raw:
            reviews.append(review.serialize())
        response = {'book_metadata':book.serialize(), 'reviews': reviews, 'related_url': related_url}
        logger.logrequest(request, response)
        return {'book_metadata':book.serialize(), 'reviews':reviews, 'related_url':related_url}
    else:
        err_msg = 'Book not found.'
        logger.logrequest(request)
        return redirect(url_for('.get_meta_data', msg=err_msg))

@book_app.route('/api/allbooks', methods=['GET','POST'])
def get_all_books_endpoint():
    msg=''
    if request.args:
        msg= request.args['msg']

    first_10_books = get_first_10_books()
    books =[]
    for book in first_10_books:
        books.append(book.serialize())
    retjson = jsonify(books)
    logger.logrequest(request, books)
    return retjson



#add a book review
@book_app.route('/api/addreview', methods=['POST'])
def add_review():
    req = request.get_json(force=True)
    name = req['name']
    asin = req['asin']
    summary = req['summary']
    review = Review(asin, summary,name)
    if get_book_by_asin(asin):
        db.session.add(review)
        db.session.commit()
        return {'added': 'true'}
    return {'added':'false'}
    # if request.method == 'POST':
    #     asin = request.form['asin']
    #     summary = request.form['summary']
    #     print(request.form['summary'])
    #     print(summary)

    #     print(f'review_id: {review.id}')
    #     return f'review_id: {review.id}'
#add a book review
@book_app.route('/api/deletereview/<id>', methods=['POST','DELETE'])
def delete_review(id):
    return str(deleteReview(id))

def get_list_asin_details(ls):
    imgUrl=[]
    books = get_book_by_asin(ls)
    for val in books:
        temp=[val.asin,val.imUrl]
        imgUrl.append(temp)
    return imgUrl