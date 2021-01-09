from functools import reduce
from operator import getitem

import pytest

from query_filter.filter import q_filter
from query_filter.query import (
    q_attrs_all,
    q_attrs_any,
    q_attrs_not_any,
    q_items_all,
    q_items_any,
    q_items_not_any,
    split_key,
)


class User:
    def __init__(self, first_name: str, last_name: str,
                 email: str, gender: str, email_confirmed: bool):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.gender = gender
        self.email_confirmed = email_confirmed


@pytest.fixture
def user_one_data():
    return {
        "first_name": "Breanne",
        "last_name": "Janosevic",
        "email": "bjanosevic0@sitemeter.com",
        "gender": "Female",
        "email_confirmed": False,
    }


@pytest.fixture
def user_one(user_one_data):
    return User(**user_one_data)


@pytest.fixture
def user_two_data():
    return {
        "first_name": "Valle",
        "last_name": "Ginman",
        "email": "vginman1@cisco.com",
        "gender": "Male",
        "email_confirmed": False,
    }


@pytest.fixture
def user_two(user_two_data):
    return User(**user_two_data)


@pytest.fixture
def user_three_data():
    return {
        "first_name": "Galven",
        "last_name": "Henriet",
        "email": "ghenriet2@un.org",
        "gender": "Male",
        "email_confirmed": True,
    }


@pytest.fixture
def user_three(user_three_data):
    return User(**user_three_data)


@pytest.fixture
def user_four_data():
    return {
        "first_name": "Krystalle",
        "last_name": "Philipeaux",
        "email": "kphilipeaux3@macromedia.com",
        "gender": "Female",
        "email_confirmed": False,
    }


@pytest.fixture
def user_four(user_four_data):
    return User(**user_four_data)


@pytest.fixture
def user_five_data():
    return {
        "first_name": "Giordano",
        "last_name": "Cristou",
        "email": "gcristou4@si.edu",
        "gender": "Male",
        "email_confirmed": True,
    }


@pytest.fixture
def user_five(user_five_data):
    return User(**user_five_data)


@pytest.fixture
def users_data(user_one_data, user_two_data, user_three_data,
               user_four_data, user_five_data):
    return (user_one_data, user_two_data, user_three_data,
            user_four_data, user_five_data)


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
def test_split_attr_key_fails_if_not_formatted_correctly(key):
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


def test_q_items_all(users_data, user_one_data, user_four_data):
    expected = [user_one_data, user_four_data]

    results = q_filter(users_data, q_items_all(gender="Female"))

    assert list(results) == expected


def test_q_items_all_two_args(users_data, user_four_data):
    expected = [user_four_data]

    results = q_filter(users_data,
                       q_items_all(gender="Female",
                                   last_name="Philipeaux"))

    assert list(results) == expected


def test_q_items_all_empty_results(users_data):
    expected = []

    results = q_filter(users_data,
                       q_items_all(gender="Female",
                                   last_name="Philipeaux",
                                   email="gcristou4@si.edu"))

    assert list(results) == expected


def test_q_items_any(users_data, user_one_data,
                     user_two_data, user_four_data):

    expected = [user_one_data, user_two_data, user_four_data]

    results = q_filter(users_data,
                       q_items_any(gender="Female",
                                   email_confirmed__is=False))

    assert list(results) == expected


def test_q_items_not_any(users_data, user_three_data, user_five_data):

    expected = [user_three_data, user_five_data]

    results = q_filter(users_data,
                       q_items_not_any(gender="Female",
                                       email_confirmed__is_not=True))

    assert list(results) == expected


def test_q_attrs_all(users, user_one, user_two, user_four):
    expected = [user_one, user_two, user_four]

    results = q_filter(users, q_attrs_all(email__regex=r"\.com"))

    assert list(results) == expected


def test_q_attrs_all_not(users, user_two):
    # Outcome should be same as q_not_any below
    expected = [user_two]

    results = q_filter(users,
                       q_attrs_not_any(gender="Female",
                                       email_confirmed__is=True))

    assert list(results) == expected


def test_q_attrs_any(users, user_one, user_three, user_four, user_five):

    expected = [user_one, user_three, user_four, user_five]

    results = q_filter(users,
                       q_attrs_any(gender="Female",
                                   email_confirmed__is=True))

    assert list(results) == expected


def test_q_attrs_any_not(users, user_two):

    expected = [user_two]

    results = q_filter(users,
                       q_attrs_not_any(gender="Female",
                                       email_confirmed__is=True))

    assert list(results) == expected


def test_q_attrs_not_any(users, user_two):
    expected = [user_two]

    results = q_filter(users,
                       q_attrs_not_any(gender="Female",
                                       email_confirmed__is=True))

    assert list(results) == expected
