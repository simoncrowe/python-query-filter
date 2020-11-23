import pytest

from query_filter.filter import item_filter
from query_filter.path import Path


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
def addresses(address_one, address_two, address_three, address_four, address_five):
    return [
        address_one, address_two, address_three, address_four, address_five
    ]


def test_quality(addresses, address_two, address_three, address_four):
    expected = [address_two, address_three, address_four]

    actual = list(item_filter(addresses, Path("state") == "California"))

    assert actual == expected
