from itertools import product
from test import client

import pytest
import test_data

import api.http_status_codes as status_code


def _get_query_string(query_parameters: dict) -> str:
    query_string = ""
    possible_parameters = [
        "author",
        "category",
        "top",
        "isbn",
        "min_rating",
        "max_rating",
    ]

    for p in possible_parameters:
        if p in query_parameters and query_parameters[p] is not None:
            query_string += f"{p}={query_parameters[p]}&"

    return query_string[:-1]


def _get_combinations(book_attribute_values: list) -> list:
    all_valid_values = []

    for i in range(len(book_attribute_values)):
        all_valid_values.append((book_attribute_values[i], None))

    return list(product(*all_valid_values))


@pytest.mark.parametrize("isbn", test_data.INVALID_ISBNS)
def test_query_fails_when_isbn_invalid(isbn):
    response = client.get(f"/books/q?isbn={isbn}")
    assert response.status_code == status_code.UNPROCESSABLE_ENTITY


@pytest.mark.parametrize(
    (
        "author",
        "category",
        "top",
        "isbn",
        "min_rating",
        "max_rating",
    ),
    _get_combinations(
        ["Stephen Hawking", "Science", 1, test_data.VALID_ISBN, 3.5, 4.5]
    ),
)
def test_query_combinations_that_return_results(
    mocker,
    author: str,
    category: str,
    top: int,
    isbn: str,
    min_rating: float,
    max_rating: float,
):
    mock_books = [
        dict(
            isbn=test_data.VALID_ISBN,
            title="A Brief History of Time",
            author="Stephen Hawking",
            category="Science",
            avg_rating=4.3,
            num_ratings=0,
            sum_ratings=0,
            soft_deleted=False,
        )
    ]

    test_data.setup_mock_books(mocker, mock_books)
    query_parameters = dict(
        author=author,
        category=category,
        top=top,
        isbn=isbn,
        min_rating=min_rating,
        max_rating=max_rating,
    )
    query_string = _get_query_string(query_parameters)

    response = client.get(f"/books/q?{query_string}")
    assert response.status_code == status_code.OK

    books = list(response.json())
    assert books == mock_books


def test_zero_not_a_valid_value_for_top():
    response = client.get("/books/q?top=0")
    assert response.status_code == status_code.UNPROCESSABLE_ENTITY


@pytest.mark.parametrize(
    (
        "author",
        "category",
        "isbn",
        "min_rating",
        "max_rating",
    ),
    _get_combinations(["John Doe", "Biography", "0000000000000", 1, 4]),
)
def test_query_combinations_that_return_no_results(
    mocker, author: str, category: str, isbn: str, min_rating: float, max_rating: float
):
    if min_rating is None or max_rating is None:
        return

    mock_books = [
        dict(
            isbn=test_data.VALID_ISBN,
            title="A Brief History of Time",
            author="Stephen Hawking",
            category="Science",
            avg_rating=4.3,
            num_ratings=0,
            sum_ratings=0,
            soft_deleted=False,
        )
    ]

    test_data.setup_mock_books(mocker, mock_books)

    query_parameters = dict(
        author=author,
        category=category,
        top=None,
        isbn=isbn,
        min_rating=min_rating,
        max_rating=max_rating,
    )

    query_string = _get_query_string(query_parameters)

    response = client.get(f"/books/q?{query_string}")
    assert response.status_code == status_code.OK

    assert response.json() == []


@pytest.mark.parametrize(("min_rating", "max_rating"), [(5.0, 1.0), (3.0, 3.0)])
def test_return_bad_request_when_max_rating_is_less_than_or_equal_to_min_rating(
    min_rating: float, max_rating: float
):
    query_parameters = dict(
        author="John Doe",
        category="Cooking",
        top=None,
        isbn=test_data.VALID_ISBN,
        min_rating=min_rating,
        max_rating=max_rating,
    )

    query_string = _get_query_string(query_parameters)

    response = client.get(f"/books/q?{query_string}")
    assert response.status_code == status_code.BAD_REQUEST
