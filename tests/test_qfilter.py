import pytest

from query_filter.filter import (
    item,
    qall,
    qany,
    qfilter_all,
    qfilter_any,
    qfilter_not_any,
    qnot,
)


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


def test_qfilter_all_with_two_predicates(all_trials, trial_one):
    expected = [trial_one]

    results = qfilter_all(all_trials,
                         item("survived") == True,
                         item("date").contains("2003"))

    assert list(results) == expected


def test_qfilter_all_with_three_predicates(all_trials, trial_three):
    expected = [trial_three]

    results = qfilter_all(all_trials,
                         item("survived") == False,
                         item("drug") == "tolterodine tartrate",
                         item("dose_mg") > 350)

    assert list(results) == expected


def test_qfilter_any_with_two_predicates(
    all_trials, trial_one, trial_two, trial_three
):
    expected = [trial_one, trial_two, trial_three]

    results = qfilter_any(all_trials,
                         item("survived") == True,
                         item("date").contains("2003"))

    assert list(results) == expected


def test_qfilter_any_with_three_predicates(
    all_trials, trial_two, trial_three, trial_four, trial_five
):
    expected = [trial_two, trial_three, trial_four, trial_five]

    results = qfilter_any(all_trials,
                         item("survived") == False,
                         item("drug") == "tolterodine tartrate",
                         item("dose_mg") > 350)

    assert list(results) == expected


def test_qfilter_not_any_with_two_predicates(all_trials, trial_four, trial_five):
    expected = [trial_four, trial_five]

    results = qfilter_not_any(all_trials,
                             item("survived") == True,
                             item("date").contains("2003"))

    assert list(results) == expected


def test_qfilter_not__any_with_three_predicates(all_trials, trial_one):
    expected = [trial_one]

    results = qfilter_not_any(all_trials,
                             item("survived") == False,
                             item("drug") == "tolterodine tartrate",
                             item("dose_mg") > 350)

    assert list(results) == expected


def test_qall_with_two_predicates(all_trials, trial_one):
    expected = [trial_one]

    results = qfilter_all(all_trials,
                          qall(item("survived") == True,
                              item("date").contains("2003")))

    assert list(results) == expected


def test_qall_with_three_predicates(all_trials, trial_three):
    expected = [trial_three]

    results = qfilter_all(all_trials,
                          qall(item("survived") == False,
                               item("drug") == "tolterodine tartrate",
                               item("dose_mg") > 350))

    assert list(results) == expected


def test_qany_with_two_predicates(
    all_trials, trial_one, trial_two, trial_three
):
    expected = [trial_one, trial_two, trial_three]

    results = qfilter_all(all_trials,
                          qany(item("survived") == True,
                              item("date").contains("2003")))

    assert list(results) == expected


def test_qany_with_three_predicates(
    all_trials, trial_two, trial_three, trial_four, trial_five
):
    expected = [trial_two, trial_three, trial_four, trial_five]

    results = qfilter_all(all_trials,
                          qany(item("survived") == False,
                              item("drug") == "tolterodine tartrate",
                              item("dose_mg") > 350))

    assert list(results) == expected


def test_qnot(all_trials, trial_one, trial_two):
    expected = [trial_one, trial_two]

    results = qfilter_all(all_trials,
                          qnot(item("survived") == False))

    assert list(results) == expected


def test_qnot_with_qany_and_two_predicates(all_trials, trial_four, trial_five):
    expected = [trial_four, trial_five]

    results = qfilter_all(all_trials,
                          qnot(qany(item("survived") == True,
                                   item("date").contains("2003"))))

    assert list(results) == expected


def test_qnot_with_qany_and_three_predicates(all_trials, trial_one):
    expected = [trial_one]

    results = qfilter_all(all_trials,
                          qnot(qany(item("survived") == False,
                                   item("drug") == "tolterodine tartrate",
                                   item("dose_mg") > 350)))

    assert list(results) == expected


def test_qnot_with_qall(
    all_trials, trial_one, trial_two, trial_four, trial_five
):
    expected = [trial_one, trial_two, trial_four, trial_five]

    results = qfilter_all(all_trials,
                          qnot(qall(item("date").contains("2003"),
                                    item("dose_mg") > 400)))

    assert list(results) == expected
