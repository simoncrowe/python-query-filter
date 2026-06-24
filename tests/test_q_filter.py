import pytest

from query_filter import (q, q_all, q_any, q_contains, q_filter_all,
                          q_filter_any, q_filter_not_any, q_not)


@pytest.fixture
def trial_one():
    return {
        "id": 1,
        "date": "2003-04-11",
        "species": "Streptopelia senegalensis",
        "drug": "HELMINTHOSPORIUM SOROKINIANUM",
        "dose_mg": 67.9,
        "survived": True
    }


@pytest.fixture
def trial_two():
    return {
        "id": 2,
        "date": "2013-05-20",
        "species": "Geococcyx californianus",
        "drug": "ENSULIZOLE, OCTINOXATE, and TITANIUM DIOXIDE",
        "dose_mg": 829.66,
        "survived": True
    }


@pytest.fixture
def trial_three():
    return {
        "id": 3,
        "date": "2003-08-09",
        "species": "Neophron percnopterus",
        "drug": "tolterodine tartrate",
        "dose_mg": 421.28,
        "survived": False
    }


@pytest.fixture
def trial_four():
    return {
        "id": 4,
        "date": "2017-06-19",
        "species": "Merops nubicus",
        "drug": "Lorazepam",
        "dose_mg": 377.18,
        "survived": False
    }


@pytest.fixture
def trial_five():
    return {
        "id": 5,
        "date": "2016-12-12",
        "species": "Dasypus novemcinctus",
        "drug": "Nicotine Polacrilex",
        "dose_mg": 147.47,
        "survived": False
    }


@pytest.fixture
def all_trials(trial_one, trial_two, trial_three, trial_four, trial_five):
    return [trial_one, trial_two, trial_three, trial_four, trial_five]


def test_q_filter_all_with_two_predicates(all_trials, trial_one):
    expected = [trial_one]

    results = q_filter_all(all_trials,
                           q["survived"],
                           q_contains(q["date"], "2003"))

    assert list(results) == expected


def test_q_filter_all_with_three_predicates(all_trials, trial_three):
    expected = [trial_three]

    results = q_filter_all(all_trials,
                           ~q["survived"],
                           q["drug"] == "tolterodine tartrate",
                           q["dose_mg"] > 350)

    assert list(results) == expected


def test_q_filter_any_with_two_predicates(
    all_trials, trial_one, trial_two, trial_three
):
    expected = [trial_one, trial_two, trial_three]

    results = q_filter_any(all_trials,
                           q["survived"],
                           q_contains(q["date"], "2003"))

    assert list(results) == expected


def test_q_filter_any_with_three_predicates(
    all_trials, trial_two, trial_three, trial_four, trial_five
):
    expected = [trial_two, trial_three, trial_four, trial_five]

    results = q_filter_any(all_trials,
                           ~q["survived"],
                           q["drug"] == "tolterodine tartrate",
                           q["dose_mg"] > 350)

    assert list(results) == expected


def test_q_filter_not_any_with_two_predicates(
    all_trials, trial_four, trial_five
):
    expected = [trial_four, trial_five]

    results = q_filter_not_any(all_trials,
                               q["survived"],
                               q_contains(q["date"], "2003"))

    assert list(results) == expected


def test_q_filter_not__any_with_three_predicates(all_trials, trial_one):
    expected = [trial_one]

    results = q_filter_not_any(all_trials,
                               ~q["survived"],
                               q["drug"] == "tolterodine tartrate",
                               q["dose_mg"] > 350)

    assert list(results) == expected


def test_all_with_two_predicates(all_trials, trial_one):
    expected = [trial_one]

    results = q_filter_all(all_trials,
                           q_all(q["survived"],
                                 q_contains(q["date"], "2003")))

    assert list(results) == expected


def test_all_with_three_predicates(all_trials, trial_three):
    expected = [trial_three]

    results = q_filter_all(all_trials,
                           q_all(~q["survived"],
                                 q["drug"] == "tolterodine tartrate",
                                 q["dose_mg"] > 350))

    assert list(results) == expected


def test_any_with_two_predicates(
    all_trials, trial_one, trial_two, trial_three
):
    expected = [trial_one, trial_two, trial_three]

    results = q_filter_all(all_trials,
                           q_any(q["survived"],
                                 q_contains(q["date"], "2003")))

    assert list(results) == expected


def test_any_with_three_predicates(
    all_trials, trial_two, trial_three, trial_four, trial_five
):
    expected = [trial_two, trial_three, trial_four, trial_five]

    results = q_filter_all(all_trials,
                           q_any(q_not(q["survived"]),
                                 q["drug"] == "tolterodine tartrate",
                                 q["dose_mg"] > 350))

    assert list(results) == expected


def test_not(all_trials, trial_one, trial_two):
    expected = [trial_one, trial_two]

    results = q_filter_all(all_trials,
                           q_not(~q["survived"]))

    assert list(results) == expected


def test_not_with_any_and_two_predicates(all_trials, trial_four, trial_five):
    expected = [trial_four, trial_five]

    results = q_filter_all(all_trials,
                           q_not(q_any(q["survived"],
                                       q_contains(q["date"], "2003"))))

    assert list(results) == expected


def test_not_with_any_and_three_predicates(all_trials, trial_one):
    expected = [trial_one]

    results = q_filter_all(
        all_trials,
        q_not(
            q_any(
                ~q["survived"],
                q["drug"] == "tolterodine tartrate",
                q["dose_mg"] > 350
            )
        )
    )

    assert list(results) == expected


def test_not_with_all(
    all_trials, trial_one, trial_two, trial_four, trial_five
):
    expected = [trial_one, trial_two, trial_four, trial_five]

    results = q_filter_all(all_trials,
                           q_not(q_all(q_contains(q["date"], "2003"),
                                       q["dose_mg"] > 400)))

    assert list(results) == expected
