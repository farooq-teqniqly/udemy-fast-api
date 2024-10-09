import re

from fastapi import HTTPException


def validate_isbn(isbn: str):
    """
    Validates whether the provided ISBN is a 13-digit numeric string.

    Args:
        isbn: A string representing the ISBN to be validated.

    Raises:
        HTTPException: If the ISBN is not exactly 13 numeric digits.

    Returns:
        The validated ISBN string if it meets the 13-digit numeric criteria.
    """
    if not re.fullmatch(r"\d{13}", isbn):
        raise HTTPException(
            status_code=400, detail="Invalid ISBN. It must be 13 numeric digits."
        )
    return isbn
