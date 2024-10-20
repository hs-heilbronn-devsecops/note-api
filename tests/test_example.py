# tests/test_example.py

from note_api.example import add, subtract

def test_add():
    assert add(3, 2) == 5
    assert add(-1, 1) == 0

def test_subtract():
    assert subtract(5, 3) == 2
    assert subtract(10, 5) == 5
