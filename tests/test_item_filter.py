import pytest

from query_filter.filter import Item, qfilter


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


def test_equal(addresses, address_two, address_three, address_four):
    expected = [address_two, address_three, address_four]

    actual = list(qfilter(addresses, Item("state") == "California"))

    assert actual == expected


def test_not_equal(addresses, address_one, address_five):
    expected = [address_one, address_five]

    actual = list(qfilter(addresses, Item("state") != "California"))

    assert actual == expected


def test_less_than(addresses, address_one, address_two):
    expected = [address_one, address_two]

    actual = list(qfilter(addresses, Item("id") < 3))

    assert actual == expected


def test_less_than_or_equal(addresses, address_one,
                            address_two, address_three):
    expected = [address_one, address_two, address_three]

    actual = list(qfilter(addresses, Item("id") <= 3))

    assert actual == expected


def test_greater_than(addresses, address_four, address_five):
    expected = [address_four, address_five]

    actual = list(qfilter(addresses, Item("id") > 3))

    assert actual == expected


def test_greater_than_or_equal(addresses, address_three,
                               address_four, address_five):
    expected = [address_three, address_four, address_five]

    actual = list(qfilter(addresses, Item("id") >= 3))

    assert actual == expected

def test_is_in_list(addresses, address_one, address_five):
    expected = [address_one, address_five]

    actual = list(
        qfilter(addresses, Item("state").is_in(["Texas", "Massachusetts"]))
    )

    assert actual == expected


def test_is_in_string(addresses, address_one, address_two):
    expected = [address_one, address_two]

    actual = list(
        qfilter(addresses, Item("post_code").is_in("92415-241024-01152"))
    )

    assert actual == expected


def test_list_contains(addresses, address_one, address_two):
    primes =  {"type": "prime", "numbers": [2, 3, 5, 7, 11]}
    odd = {"type": "odd", "numbers": [1, 3, 5, 7, 9]}
    even = {"type": "even", "numbers": [0, 2, 4, 6, 8]}

    sequences = [primes, odd, even]
    expected = [primes, even]

    actual = list(qfilter(sequences, Item("numbers").contains(2)))

    assert actual == expected



def test_string_contains(addresses, address_one, address_five):
    torpid_dic = {"type": "adjective", "word": "torpid"}
    turbid_dic = {"type": "adjective", "word": "turbid"}
    turgid_dic = {"type": "adjective", "word": "turgid"}
    words = [torpid_dic, turbid_dic, turgid_dic]
    expected = [turbid_dic, turgid_dic]

    actual = list(qfilter(words, Item("word").contains("u")))

    assert actual == expected

