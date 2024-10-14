from test import client

import test_data

import api.http_status_codes as status_code


def test_can_add_review_to_book(mocker):
    test_data.setup_mock_books(mocker)
    mock_reviews = test_data.setup_mock_reviews(mocker)
    review_text = "This is a great book!"
    request = dict(review=review_text)
    response = client.post(f"/books/{test_data.VALID_ISBN}/reviews", json=request)
    assert response.status_code == status_code.OK
    assert any(review_text in review_data["reviews"] for review_data in mock_reviews)
