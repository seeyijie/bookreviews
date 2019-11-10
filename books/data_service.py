from models.BooksMetaData import BookMetaData


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