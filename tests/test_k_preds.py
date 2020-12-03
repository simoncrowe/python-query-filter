from functools import reduce
from operator import getitem

import pytest

from query_filter.filter import q_filter
from query_filter.query import (
    k_attrs_all,
    k_attrs_any,
    k_attrs_not_any,
    k_items_all,
    k_items_any,
    k_items_not_any,
    split_key,
)

@pytest.fixture
def user_one():
    return {
        "id": 1,
        "first_name": "Breanne",
        "last_name": "Janosevic",
        "email": "bjanosevic0@sitemeter.com",
        "gender": "Female",
    }


@pytest.fixture
def user_two():
    return {
        "id": 2,
        "first_name": "Valle",
        "last_name": "Ginman",
        "email": "vginman1@cisco.com",
        "gender": "Male",
    }


@pytest.fixture
def user_three():
    return {
        "id": 3,
        "first_name": "Galven",
        "last_name": "Henriet",
        "email": "ghenriet2@un.org",
        "gender": "Male",
    }


@pytest.fixture
def user_four():
    return {
        "id": 4,
        "first_name": "Krystalle",
        "last_name": "Philipeaux",
        "email": "kphilipeaux3@macromedia.com",
        "gender": "Female",
    }


@pytest.fixture
def user_five():
    return {
        "id": 5,
        "first_name": "Giordano",
        "last_name": "Cristou",
        "email": "gcristou4@si.edu",
        "gender": "Male",
    }


@pytest.fixture
def users(user_one, user_two, user_three, user_four, user_five):
    return (user_one, user_two, user_three, user_four, user_five)


def get(obj, *keys):
    """Simple item getter for testing purposes."""
    return reduce(getitem, keys, obj)


@pytest.mark.parametrize(
    "key",
    ["__", "___", "_____ ", "__lt", "a__", "a__b__", "__a__gt"]
)
def test_split_key_fails_if_not_formatted_correctly(key):
    with pytest.raises(ValueError):
        split_key(key)


@pytest.mark.parametrize(
    "key,expected",
    [
        ("a", (["a"], "eq")),
        ("a__b", (["a", "b"], "eq")),
        ("a__b__c", (["a", "b", "c"], "eq")),
        ("a__lte", (["a"], "lte")),
        ("a__b__gte", (["a", "b"], "gte")),
        ("a__b__c__in", (["a", "b", "c"], "in")),
    ]
)
def test_split_key_produces_expected_results(key, expected):
    result = split_key(key)
    assert result == expected


def test_k_items_all(users, user_one, user_four):
    expected = [user_one, user_four]

    results = q_filter(users, k_items_all(gender="Female"))

    assert list(results) == expected


def test_k_items_all_two_args(users, user_four):
    expected = [user_four]

    results = q_filter(users,
                       k_items_all(gender="Female",
                                   last_name="Philipeaux"))

    assert list(results) == expected


def test_k_items_all_empty_results(users):
    expected = []

    results = q_filter(users,
                       k_items_all(gender="Female",
                                   last_name="Philipeaux",
                                   email="gcristou4@si.edu"))

    assert list(results) == expected
