import json
from test import client

import pytest
import test_data
from starlette import status


def test_create_book_is_successful(mocker):
    request = dict(
        title="The Great Gatsby",
        author="F. Scott Fitzgerald",
        isbn=test_data.VALID_ISBN,
        category="Classics",
    )

    response = client.post("/books", json=request)
    assert response.status_code == status.HTTP_201_CREATED

    created_book = response.json()
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
        (None, "Stephen King", test_data.VALID_ISBN, "Horror"),
        ("", "Stephen King", test_data.VALID_ISBN, "Horror"),
        ("The Stand", None, test_data.VALID_ISBN, "Horror"),
        ("The Stand", "", test_data.VALID_ISBN, "Horror"),
        ("The Stand", "Stephen King", None, "Horror"),
        ("The Stand", "Stephen King", "", "Horror"),
        ("The Stand", "Stephen King", test_data.VALID_ISBN, None),
        ("The Stand", "Stephen King", test_data.VALID_ISBN, ""),
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
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.parametrize("isbn", test_data.INVALID_ISBNS)
def test_create_book_fails_wth_invalid_isbn(isbn):
    request = dict(
        title="The Stand",
        author="Stephen King",
        isbn=isbn,
        category="Horror",
    )

    response = client.post("/books", json=json.dumps(request))
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
