import pytest

from query_filter import query
from query_filter.filter import q_filter

# Using a Query instance to test the public API
q = query.Query()


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
        "address": "1 Moth Park",
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


def test_equal(addresses, address_two, address_three, address_four):
    expected = [address_two, address_three, address_four]

    results = q_filter(addresses, q["state"] == "California")

    assert list(results) == expected


def test_not_equal(addresses, address_one, address_five):
    expected = [address_one, address_five]

    results = q_filter(addresses, q["state"] != "California")

    assert list(results) == expected


def test_less_than(addresses, address_one, address_two):
    expected = [address_one, address_two]

    results = q_filter(addresses, q["id"] < 3)

    assert list(results) == expected


def test_less_than_or_equal(addresses, address_one,
                            address_two, address_three):
    expected = [address_one, address_two, address_three]

    results = q_filter(addresses, q["id"] <= 3)

    assert list(results) == expected


def test_greater_than(addresses, address_four, address_five):
    expected = [address_four, address_five]

    results = q_filter(addresses, q["id"] > 3)

    assert list(results) == expected


def test_greater_than_or_equal(addresses, address_three,
                               address_four, address_five):
    expected = [address_three, address_four, address_five]

    results = q_filter(addresses, q["id"] >= 3)

    assert list(results) == expected


def test_q_is_in_with_list(addresses, address_one, address_five):
    expected = [address_one, address_five]

    results = q_filter(
        addresses, query.q_is_in(q["state"], ["Texas", "Massachusetts"])
    )

    assert list(results) == expected


def test_q_is_in_with_string(addresses, address_one, address_two):
    expected = [address_one, address_two]

    results = q_filter(addresses, query.q_is_in(q["post_code"], "92415-241024-01152"))

    assert list(results) == expected


def test_q_contains_with_list():
    primes = {"type": "prime", "numbers": [2, 3, 5, 7, 11]}
    odd = {"type": "odd", "numbers": [1, 3, 5, 7, 9]}
    even = {"type": "even", "numbers": [0, 2, 4, 6, 8]}
    sequences = [primes, odd, even]
    expected = [primes, even]

    results = q_filter(sequences, query.q_contains(q["numbers"], 2))

    assert list(results) == expected


def test_q_contains_with_string():
    torpid_dic = {"type": "adjective", "word": "torpid"}
    turbid_dic = {"type": "adjective", "word": "turbid"}
    turgid_dic = {"type": "adjective", "word": "turgid"}
    words = [torpid_dic, turbid_dic, turgid_dic]

    expected = [turbid_dic, turgid_dic]

    actual = list(q_filter(words, query.q_contains(q["word"], "u")))

    assert actual == expected


def test_q_is():
    sentinel = object()
    ordinary_object = object()
    objects = [sentinel, ordinary_object]
    expected = [sentinel]

    actual = list(q_filter(objects, query.q_is(q, sentinel)))

    assert actual == expected


def test_q_is_not():
    sentinel = object()
    ordinary_object = object()
    objects = [sentinel, ordinary_object]
    expected = [ordinary_object]

    actual = list(q_filter(objects, query.q_is_not(q, sentinel)))

    assert actual == expected


def test_q_matches_regex():
    datum_one = {"id": 0, "value": "03/12/2020"}
    datum_two = {"id": 1, "value": "2020-12-03"}
    data = [datum_one, datum_two]
    expected = [datum_two]

    results = q_filter(data,
                       query.q_matches_regex(q["value"],
                                             r"[0-9]{4}-[0-9]{2}-[0-9]{2}"))

    assert list(results) == expected


def test_nonexistent_key(addresses):
    results = q_filter(addresses, query.q_is(["guard_dog"], None))
    assert list(results) == []


def test_query_not_callable(addresses):
    with pytest.raises(TypeError):
        q_filter(addresses, q.is_for_sale())


def test_query_not_callable_with_lookup(addresses):
    with pytest.raises(TypeError):
        q_filter(addresses, q.state.is_republican())


def test_retrieve_value_attr():
    value = "bar"
    baz_cls = type("Baz", () , {"foo": value})
    attr_lookup = query.Lookup(lookup_type=query.LookupType.ATTR, key="foo")

    result = query.retrieve_value(baz_cls, attr_lookup)

    assert result == value


def test_retrieve_value_item():
    value = "bar"
    data = {"foo": value}
    item_lookup = query.Lookup(lookup_type=query.LookupType.ITEM, key="foo")

    result = query.retrieve_value(data, item_lookup)

    assert result == value


def test_retrieve_value_invalid_lookup_type():
    with pytest.raises(ValueError):
        query.retrieve_value(object(),
                             query.Lookup(lookup_type=3.14, key="irrelevant"))
