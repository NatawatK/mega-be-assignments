import pytest

from algo.main import solve

def test_solve():
    result = solve(["ab", "cd"], 'abcd')
    assert result == ("ab","cd")


def test_solve_1():
    result = solve(["ab", "bc", "cd"], 'abcd')
    assert result == ("ab","cd")

def test_solve_2():
    result = solve(["ab", "bc", "cd"], 'cdab')
    assert result == ("cd","ab")

def test_solve_3():
    result = solve(["abc", "bc", "bcd"], 'abcbcd')
    assert result == ("abc","bcd")

def test_solve_not_found():
    result = solve(["ab", "bc", "cd"], "abab")
    assert result == None