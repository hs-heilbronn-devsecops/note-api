# import pytest

# from note_api.example import hello

# @pytest.mark.parametrize(
#     ("name", "expected"),
#     [
#         ("A. Musing", "Hello A. Musing!"),
#         ("traveler", "Hello traveler!"),
#         ("projen developer", "Hello projen developer!"),
#     ],
# )
# def test_hello(name, expected):
#     """Example test with parametrization."""
#     assert hello(name) == expected

import pytest
@pytest.mark.parametrize(
    ("name", "expected"),
    [
        ("A. Musing", "Hello A. Musing!"),
        ("traveler", "Hello traveler!"),
        ("projen developer", "Hello projen developer!"),
    ],
)
def test_hello(name, expected):
    """Example test with parametrization."""
    assert hello(name) == expected
