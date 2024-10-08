import pytest

from app import add


@pytest.mark.parametrize(
    ("x", "y", "expected"),
    [
        (3, 5, 8),
        (1.5, 2.5, 4.0),
        (1, 2.5, 3.5),
        (-3, -2, -5),
        (0, 5, 5),
    ],
)
def test_add(x, y, expected):
    assert add(x, y) == expected
