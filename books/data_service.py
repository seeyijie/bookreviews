from models.BooksMetaData import BookMetaData

from books.models import Reviews
from models.Title import Title
from application import db

def get_first_10_books():
    query = BookMetaData.objects[:10]
    return list(query)

def get_book_by_asin(book_asin):
        if isinstance(book_asin, str):
            query = BookMetaData.objects.filter(asin = book_asin)
            return list(query)
        else:
            query = BookMetaData.objects.filter(asin__in = book_asin)
            return list(query)

def deleteReview(id):
    print(id)
    obj = Reviews.query.filter_by(id=int(id)).one_or_none()
    if obj:
        db.session.delete(obj)
        db.session.commit()
        return {'deleted': 'true'}
    return {'deleted': 'false'}

def addBook(asin,imUrl,salesRank,title,related, categories,description, price):
    if not get_book_by_asin(asin):
        titleEntry = Title(asin= asin, title= title)
        db.session.add(titleEntry)
        db.session.commit()
        book = BookMetaData(asin=asin,imUrl=imUrl,salesRank=salesRank,text=title,related=related, categories=categories,description=description, price=price)
        book.save()
        return {'added': 'true'}
    return {'added':'false'}