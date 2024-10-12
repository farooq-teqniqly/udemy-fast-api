from test import client

import api.http_status_codes as status_code
from api.models import CreateBookRequest


def _setup_mock_books(mocker, books):
    mocker.patch("api.book_service.BOOKS", books)


def test_create_book_is_successful(mocker):
    mock_books = []
    _setup_mock_books(mocker, mock_books)

    request = CreateBookRequest(
        title="The Great Gatsby",
        author="F. Scott Fitzgerald",
        isbn="9780743273565",
        category="Classics",
    )

    response = client.post("/books", json=request.model_dump())
    assert response.status_code == status_code.OK

    created_book = mock_books[0]
    assert created_book["title"] == request.title
    assert created_book["author"] == request.author
    assert created_book["isbn"] == request.isbn
    assert created_book["category"] == request.category
    assert created_book["avg_rating"] is None
    assert created_book["num_ratings"] is None
    assert created_book["soft_deleted"] is False
