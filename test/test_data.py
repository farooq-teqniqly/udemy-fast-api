INVALID_ISBNS = ["fffffffff1111", "fffffffffffff", "111111111111", "111111111111111"]
VALID_ISBN = "4444444444444"

MOCK_BOOKS = [
    dict(
        isbn=VALID_ISBN,
        title="A Brief History of Time",
        author="Stephen Hawking",
        category="Science",
        avg_rating=None,
        num_ratings=0,
        sum_ratings=0,
        soft_deleted=False,
    )
]


def setup_mock_books(mocker, books=None) -> dict:
    if books is None:
        books = MOCK_BOOKS
    mocker.patch("api.book_service.BOOKS", books)
    return books
