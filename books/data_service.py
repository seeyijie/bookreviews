from books.models import BookMetaData


def get_first_10_books():
    query = BookMetaData.objects[:10]
    return list(query)

def get_book_by_asin(book_asin):
    query = BookMetaData.objects.filter(asin= book_asin)
    return list(query)