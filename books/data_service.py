from books.models import BookMetaData


def get_first_10_books():
    query = BookMetaData.objects().filter(asin="B000FA5UXC")
    books = list(query)
    return books


get_first_10_books()
