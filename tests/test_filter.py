import pytest

from query_filter.filter import query_filter


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


def test_filter_does_not_return_imput_object_references(users):
    for in_user, out_user in zip(users, query_filter(users)):
        assert in_user is not out_user


def test_filter_keyword_arg(users, user_one, user_four):
    expected = (user_one, user_four)

    results = tuple(query_filter(users, gender="Female"))

    assert results == expected


def test_filter_keyword_args(users, user_four):
    expected = (user_four,)

    results = tuple(
        query_filter(users, gender="Female", last_name="Philipeaux")
    )

    assert results == expected


def test_filter_keyword_args_empty_results(users):
    expected = tuple() 

    results = tuple(
        query_filter(users,
                     gender="Female",
                     last_name="Philipeaux",
                     email="gcristou4@si.edu")
    )
    
    assert results == expected


def test_predicate_arg(users, user_two, user_four):
    expected = (user_two, user_four)

    def id_is_even(item):
        return item["id"] % 2 == 0

    results = tuple(query_filter(users, id_is_even))

    assert results == expected


def test_predicate_args(users, user_one):
    expected = (user_one,)

    def id_is_odd(item):
        return item["id"] % 2 == 1

    def email_is_dot_com(item):
        return item["email"].endswith(".com")

    results = tuple(query_filter(users, id_is_odd, email_is_dot_com))

    assert results == expected


def test_predicate_arg_with_keyword_arg(users, user_two):
    expected = (user_two,)

    def id_is_even(item):
        return item["id"] % 2 == 0

    results = tuple(query_filter(users, id_is_even, gender="Male"))

    assert results == expected
