import json
from test import client

import pytest
import test_data

import api.http_status_codes as status_code

VALID_ISBN = "4444444444444"


def _setup_mock_books(mocker, books):
    mocker.patch("api.book_service.BOOKS", books)


def test_create_book_is_successful(mocker):
    mock_books = []
    _setup_mock_books(mocker, mock_books)

    request = dict(
        title="The Great Gatsby",
        author="F. Scott Fitzgerald",
        isbn=VALID_ISBN,
        category="Classics",
    )

    response = client.post("/books", json=request)
    assert response.status_code == status_code.OK

    created_book = mock_books[0]
    assert created_book["title"] == request["title"]
    assert created_book["author"] == request["author"]
    assert created_book["isbn"] == request["isbn"]
    assert created_book["category"] == request["category"]
    assert created_book["avg_rating"] is None
    assert created_book["num_ratings"] is None
    assert created_book["soft_deleted"] is False


@pytest.mark.parametrize(
    ("title", "author", "isbn", "category"),
    [
        (None, "Stephen King", VALID_ISBN, "Horror"),
        ("", "Stephen King", VALID_ISBN, "Horror"),
        ("The Stand", None, VALID_ISBN, "Horror"),
        ("The Stand", "", VALID_ISBN, "Horror"),
        ("The Stand", "Stephen King", None, "Horror"),
        ("The Stand", "Stephen King", "", "Horror"),
        ("The Stand", "Stephen King", VALID_ISBN, None),
        ("The Stand", "Stephen King", VALID_ISBN, ""),
    ],
)
def test_create_book_fails_when_request_is_missing_required_attributes(
    title, author, isbn, category
):
    request = dict(
        title=title,
        author=author,
        isbn=isbn,
        category=category,
    )

    response = client.post("/books", json=json.dumps(request))
    assert response.status_code == status_code.UNPROCESSABLE_ENTITY


@pytest.mark.parametrize("isbn", test_data.INVALID_ISBNS)
def test_create_book_fails_wth_invalid_isbn(isbn):
    request = dict(
        title="The Stand",
        author="Stephen King",
        isbn=isbn,
        category="Horror",
    )

    response = client.post("/books", json=json.dumps(request))
    assert response.status_code == status_code.UNPROCESSABLE_ENTITY
