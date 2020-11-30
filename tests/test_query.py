from functools import reduce
from operator import getitem

import pytest

from query_filter.filter import q_filter, Query


@pytest.fixture
def address_one():
    return {
        "id": 1,
        "address": "41289 Hayes Street",
        "post_code": "01152",
        "state": "Massachusetts"
    }


@pytest.fixture
def address_two():
    return {
        "id": 2,
        "address": "182 Killdeer Alley",
        "post_code": "92415",
        "state": "California"
    }


@pytest.fixture
def address_three():
    return {
        "id": 3,
        "address": "1 Amoth Park",
        "post_code": "92153",
        "state": "California"
    }


@pytest.fixture
def address_four():
    return {
        "id": 4,
        "address": "3 Park Meadow Street",
        "post_code": "93106",
        "state": "California"
    }


@pytest.fixture
def address_five():
    return {
        "id": 5,
        "address": "19 Crest Line Junction",
        "post_code": "76016",
        "state": "Texas"
    }


@pytest.fixture
def addresses(address_one, address_two, address_three,
              address_four, address_five):
    return [
        address_one, address_two, address_three, address_four, address_five
    ]


def get(obj, *keys):
    """Simple item getter for testing"""
    return reduce(getitem, keys, obj)


def test_equal(addresses, address_two, address_three, address_four):
    expected = [address_two, address_three, address_four]

    actual = list(
        q_filter(addresses,
                 Query("state", getter=get) == "California")
    )

    assert actual == expected


def test_not_equal(addresses, address_one, address_five):
    expected = [address_one, address_five]

    actual = list(
        q_filter(addresses,
                 Query("state", getter=get) != "California")
    )

    assert actual == expected


def test_less_than(addresses, address_one, address_two):
    expected = [address_one, address_two]

    actual = list(q_filter(addresses, Query("id", getter=get) < 3))

    assert actual == expected


def test_less_than_or_equal(addresses, address_one,
                            address_two, address_three):
    expected = [address_one, address_two, address_three]

    actual = list(q_filter(addresses, Query("id", getter=get) <= 3))

    assert actual == expected


def test_greater_than(addresses, address_four, address_five):
    expected = [address_four, address_five]

    actual = list(q_filter(addresses, Query("id", getter=get) > 3))

    assert actual == expected


def test_greater_than_or_equal(addresses, address_three,
                               address_four, address_five):
    expected = [address_three, address_four, address_five]

    actual = list(q_filter(addresses, Query("id", getter=get) >= 3))

    assert actual == expected


def test_is_in_list(addresses, address_one, address_five):
    expected = [address_one, address_five]

    actual = list(
        q_filter(addresses,
                 Query("state", getter=get).is_in(["Texas", "Massachusetts"]))
    )

    assert actual == expected


def test_is_in_string(addresses, address_one, address_two):
    expected = [address_one, address_two]

    actual = list(
        q_filter(
            addresses,
            Query(
                "post_code",
                getter=get
            ).is_in("92415-241024-01152")
        )
    )

    assert actual == expected


def test_list_contains():
    primes = {"type": "prime", "numbers": [2, 3, 5, 7, 11]}
    odd = {"type": "odd", "numbers": [1, 3, 5, 7, 9]}
    even = {"type": "even", "numbers": [0, 2, 4, 6, 8]}
    sequences = [primes, odd, even]

    expected = [primes, even]

    actual = list(
        q_filter(sequences,
                 Query("numbers", getter=get).contains(2))
    )

    assert actual == expected


def test_string_contains():
    torpid_dic = {"type": "adjective", "word": "torpid"}
    turbid_dic = {"type": "adjective", "word": "turbid"}
    turgid_dic = {"type": "adjective", "word": "turgid"}
    words = [torpid_dic, turbid_dic, turgid_dic]

    expected = [turbid_dic, turgid_dic]

    actual = list(
        q_filter(words,
                 Query("word", getter=get).contains("u"))
    )

    assert actual == expected


def test_is():
    class Thing:
        pass

    thing_one, thing_two = Thing(), Thing()
    thing_one_data = {"id": 0, "thing": thing_one}
    thing_two_data = {"id": 1, "thing": thing_two}
    things_data = [thing_one_data, thing_two_data]

    actual = list(
        q_filter(things_data,
                 Query("thing", getter=get)._is(thing_two))
    )

    assert len(actual) == 1
    assert actual[0]["id"] == thing_two_data["id"]


def test_is_not():
    class Thing:
        pass

    thing_one, thing_two = Thing(), Thing()
    thing_one_data = {"id": 0, "thing": thing_one}
    thing_two_data = {"id": 1, "thing": thing_two}
    things_data = [thing_one_data, thing_two_data]

    actual = list(
        q_filter(things_data,
                 Query("thing", getter=get)._is_not(thing_two))
    )

    assert len(actual) == 1
    assert actual[0]["id"] == thing_one_data["id"]
