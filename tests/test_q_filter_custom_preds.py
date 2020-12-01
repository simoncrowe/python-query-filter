import pytest

from query_filter.filter import (
    k_items_all,
    k_items_any,
    k_items_not_any,
    q_filter_all,
    q_filter_any,
    q_filter_not_any,
    q_item
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


def test_q_filter_all_custom_predicate_arg(users, user_two, user_four):
    expected = [user_two, user_four]

    def id_is_even(item):
        return item["id"] % 2 == 0

    results = q_filter_all(users, id_is_even)

    assert list(results) == expected


def test_q_filter_not_any_prediocate_arg_with_keyword_arg(
    users, user_three, user_five
):
    expected = [user_three, user_five]

    def id_is_even(item):
        return item["id"] % 2 == 0

    results = q_filter_not_any(users,
                               k_items_all(gender="Female"),
                               id_is_even)

    assert list(results) == expected


def test_k_filter_all_predicate_arg_with_keyword_arg(users, user_two):
    expected = [user_two]

    def id_is_even(item):
        return item["id"] % 2 == 0

    results = q_filter_all(users,
                           id_is_even,
                           k_items_all(gender="Male"))

    assert list(results) == expected


def test_filter_any_prediocate_arg_with_keyword_arg(
    users, user_one, user_two, user_four
):
    expected = [user_one, user_two, user_four]

    def id_is_even(item):
        return item["id"] % 2 == 0

    results = q_filter_any(users,
                           id_is_even,
                           k_items_all(gender="Female"))

    assert list(results) == expected
