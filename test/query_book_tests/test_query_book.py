from itertools import product
from test import client

import pytest
import test_data

import api.http_status_codes as status_code


def test_can_query_by_isbn(mocker):
    mock_books = test_data.setup_mock_books(mocker)
    response = client.get(f"/books/q?isbn={test_data.VALID_ISBN}")
    assert response.status_code == status_code.OK
    books = list(response.json())
    assert books[0] == mock_books[0]


@pytest.mark.parametrize("isbn", test_data.INVALID_ISBNS)
def test_query_fails_when_isbn_invalid(isbn):
    response = client.get(f"/books/q?isbn={isbn}")
    assert response.status_code == status_code.UNPROCESSABLE_ENTITY


book_attribute_values = ["Stephen Hawking", "Science", 1, test_data.VALID_ISBN]
all_valid_values = [(v, None) for v in book_attribute_values]
combinations = list(product(*[v for v in all_valid_values]))


@pytest.mark.parametrize(("author", "category", "top", "isbn"), combinations)
def test_query_combinations(mocker, author: str, category: str, top: bool, isbn: str):
    mock_books = test_data.setup_mock_books(mocker)
    query_parameters = dict(author=author, category=category, top=top, isbn=isbn)
    query_string = _get_query_string(query_parameters)

    response = client.get(f"/books/q?{query_string}")
    assert response.status_code == status_code.OK

    books = list(response.json())
    assert books == mock_books


def _get_query_string(query_parameters: dict) -> str:
    query_string = ""
    possible_parameters = ["author", "category", "top", "isbn"]

    for p in possible_parameters:
        if p in query_parameters and query_parameters[p] is not None:
            query_string += f"{p}={query_parameters[p]}&"

    return query_string[:-1]
