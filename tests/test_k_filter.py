from functools import reduce
from operator import getitem

import pytest

from query_filter.filter import k_filter_all, split_key


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


def test_k_filter_all_returns_copies_by_default(users):
    for in_user, out_user in zip(users, k_filter_all(users, get)):
        assert in_user is not out_user


def test_filter_keyword_arg(users, user_one, user_four):
    expected = (user_one, user_four)

    results = tuple(k_filter_all(users, get, gender="Female"))

    assert results == expected


def test_filter_keyword_args(users, user_four):
    expected = (user_four,)

    results = tuple(
        k_filter_all(users, get, gender="Female", last_name="Philipeaux")
    )

    assert results == expected


def test_filter_keyword_args_empty_results(users):
    expected = tuple()

    results = tuple(
        k_filter_all(users, get,
                     gender="Female",
                     last_name="Philipeaux",
                     email="gcristou4@si.edu")
    )

    assert results == expected


def test_predicate_arg(users, user_two, user_four):
    expected = (user_two, user_four)

    def id_is_even(item):
        return item["id"] % 2 == 0

    results = tuple(k_filter_all(users, get, id_is_even))

    assert results == expected


def test_predicate_args(users, user_one):
    expected = (user_one,)

    def id_is_odd(item):
        return item["id"] % 2 == 1

    def email_is_dot_com(item):
        return item["email"].endswith(".com")

    results = tuple(k_filter_all(users, get, id_is_odd, email_is_dot_com))

    assert results == expected


def test_predicate_arg_with_keyword_arg(users, user_two):
    expected = (user_two,)

    def id_is_even(item):
        return item["id"] % 2 == 0

    results = tuple(k_filter_all(users, get, id_is_even, gender="Male"))

    assert results == expected
