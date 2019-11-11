from flask import Blueprint,jsonify,request
from books.data_service import get_book_by_asin
from models.Title import Title

search_app = Blueprint('search_app', __name__)

@search_app.route('/api/titlematching/<titleSubstring>', methods=['GET'])
def title_matching(titleSubstring):
    # obtain log from mongoDB
    search = "%{}%".format(titleSubstring)
    titles = Title.query.filter(Title.title.like(search)).limit(10).all()
    titleDict= dict()
    for item in titles:
        titleDict[item.asin]= item.title
    lsOfBooks = get_book_by_asin(list(titleDict.keys()))

    for book in range(len(lsOfBooks)):
        lsOfBooks[book]['title']= titleDict[lsOfBooks[book]['asin']]
        lsOfBooks[book] = lsOfBooks[book].serialize()


    return jsonify(lsOfBooks)

