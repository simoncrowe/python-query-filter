from functools import reduce
from operator import getitem

import pytest

from query_filter.filter import q_filter
from query_filter.query import Query


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

    results = q_filter(addresses,
                       Query("state", getter=get) == "California")

    assert list(results) == expected


def test_not_equal(addresses, address_one, address_five):
    expected = [address_one, address_five]

    results = q_filter(addresses,
                       Query("state", getter=get) != "California")

    assert list(results) == expected


def test_less_than(addresses, address_one, address_two):
    expected = [address_one, address_two]

    results = q_filter(addresses, Query("id", getter=get) < 3)

    assert list(results) == expected


def test_less_than_or_equal(addresses, address_one,
                            address_two, address_three):
    expected = [address_one, address_two, address_three]

    results = q_filter(addresses, Query("id", getter=get) <= 3)

    assert list(results) == expected


def test_greater_than(addresses, address_four, address_five):
    expected = [address_four, address_five]

    results = q_filter(addresses, Query("id", getter=get) > 3)

    assert list(results) == expected


def test_greater_than_or_equal(addresses, address_three,
                               address_four, address_five):
    expected = [address_three, address_four, address_five]

    results = q_filter(addresses, Query("id", getter=get) >= 3)

    assert list(results) == expected


def test_is_in_list(addresses, address_one, address_five):
    expected = [address_one, address_five]

    results = q_filter(
        addresses, Query("state", getter=get).is_in(["Texas", "Massachusetts"])
    )

    assert list(results) == expected


def test_is_in_string(addresses, address_one, address_two):
    expected = [address_one, address_two]

    results = q_filter(
        addresses, Query("post_code", getter=get).is_in("92415-241024-01152")
    )

    assert list(results) == expected


def test_list_contains():
    primes = {"type": "prime", "numbers": [2, 3, 5, 7, 11]}
    odd = {"type": "odd", "numbers": [1, 3, 5, 7, 9]}
    even = {"type": "even", "numbers": [0, 2, 4, 6, 8]}
    sequences = [primes, odd, even]

    expected = [primes, even]

    results = q_filter(sequences, Query("numbers", getter=get).contains(2))

    assert list(results) == expected


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


def test_is_none():
    datum_one = {"id": 0, "value": 42}
    datum_two = {"id": 1, "value": None}
    data = [datum_one, datum_two]
    expected = [datum_two]

    results = q_filter(data, Query("value", getter=get).is_none())

    assert list(results) == expected


def test_is_not_none():
    datum_one = {"id": 0, "value": 42}
    datum_two = {"id": 1, "value": None}
    data = [datum_one, datum_two]
    expected = [datum_one]

    results = q_filter(data, Query("value", getter=get).is_not_none())

    assert list(results) == expected


def test_is_true():
    datum_one = {"id": 0, "value": False}
    datum_two = {"id": 1, "value": True}
    data = [datum_one, datum_two]
    expected = [datum_two]

    results = q_filter(data, Query("value", getter=get).is_true())

    assert list(results) == expected


def test_is_false():
    datum_one = {"id": 0, "value": False}
    datum_two = {"id": 1, "value": True}
    data = [datum_one, datum_two]
    expected = [datum_one]

    results = q_filter(data, Query("value", getter=get).is_false())

    assert list(results) == expected


def test_regex():
    datum_one = {"id": 0, "value": "03/12/2020"}
    datum_two = {"id": 1, "value": "2020-12-03"}
    data = [datum_one, datum_two]
    expected = [datum_two]

    results = q_filter(
        data, Query("value", getter=get).regex("[0-9]{4}-[0-9]{2}-[0-9]{2}")
    )
    assert list(results) == expected
