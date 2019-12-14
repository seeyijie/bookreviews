from flask import Blueprint, render_template, redirect, session, url_for, request, jsonify
from books.data_service import get_first_10_books
from books.data_service import get_nPage_10_books
from books.data_service import get_book_by_asin
from books.data_service import deleteReview
from books.data_service import addBook
from application import db
from books.models import Reviews
from users.models import Users
from models.logs import LoggerObject    # for logging
from flask_jwt_extended import jwt_required

book_app = Blueprint('book_app', __name__)
logger = LoggerObject()

@book_app.route('/api/books/<asin>', methods=['GET', 'POST'])
def get_book_endpoint(asin):
    # query asin from mongo and mysql
    book = get_book_by_asin([asin])
    print(book[0].related)# this is a dictionary

    related_url = {}
    for key in book[0].related:
        book[0].related[key] = book[0].related[key][:10] # limit to first 10
        related_url[key]=get_list_asin_details(book[0].related[key])
    # if a book is found
    if (len(book) > 0):
        book = book[0]
        response = {'book_metadata':book.serialize(), 'related_url': related_url}
        logger.logrequest(request, jsonify(response))
        return response
    else:
        err_msg = 'Book not found.'
        logger.logrequest(request)
        return redirect(url_for('.get_meta_data', msg=err_msg))

@book_app.route('/api/books/<asin>/reviews', methods=['GET'])
def get_reviews(asin):
    reviews_raw = Reviews.query.filter_by(asin=asin).all()
    reviews_raw = reviews_raw[::-1] #sort by latest
    reviews = []
    for review in reviews_raw:
        reviews.append(review.serialize())
    response = {'reviews':reviews}
    logger.logrequest(request, jsonify(response))
    return response

@book_app.route('/api/allbooks',defaults={'pgNumber': None}, methods=['GET','POST'])
@book_app.route('/api/allbooks/<pgNumber>', methods=['GET','POST'])
def get_all_books_endpoint(pgNumber):
    msg=''
    if "".__eq__(pgNumber):
        print('went thru as empty')
        first_10_books = get_first_10_books()
        books = []
        for book in first_10_books:
            books.append(book.serialize())
        retjson = jsonify(books)
        logger.logrequest(request, retjson)
        return retjson
    else:

        print(f'pgNumber is {pgNumber}')
        nPage_10_books = get_nPage_10_books(int(pgNumber))
        books = []
        print(len(nPage_10_books))
        for book in nPage_10_books:
            books.append(book.serialize())
        retjson = jsonify(books)
        logger.logrequest(request, retjson)
        return retjson





#add a book review
@book_app.route('/api/addreview', methods=['POST'])
@jwt_required
def add_review():
    req = request.get_json(force=True)
    asin = req['asin']
    id = req['reviewerID']

    users = Users.query.filter_by(id=id).all()

    if len(users) <= 0:
        abort(401)
    else:
        user = users[0]
        id = user.id
        name = user.name

    review = Reviews(asin, req['summary'], req['reviewText'], id, name)
    if get_book_by_asin(asin):
        db.session.add(review)
        db.session.commit()
        res = {'added': 'true'}
        logger.logrequest(request, jsonify(res))
        return res
    res = {'added':'false'}
    logger.logrequest(request, jsonify(res))
    return res

#add a book review
@book_app.route('/api/deletereview/<id>', methods=['POST','DELETE'])
@jwt_required
def delete_review(id):
    res = jsonify({'delete': 'yes'})
    logger.logrequest(request, res)
    return str(deleteReview(id))

def get_list_asin_details(ls):
    imgUrl=[]
    books = get_book_by_asin(ls)
    for val in books:
        temp=[val.asin,val.imUrl]
        imgUrl.append(temp)
    return imgUrl

@book_app.route('/api/addbook', methods=['POST'])
@jwt_required
def add_book():
    req = request.get_json(force=True)
    res = addBook(req['imUrl'],req['salesRank'],req['title'],req['related'],req['categories'],req['description'],req['price'])
    logger.logrequest(request, jsonify(res))
    return res
