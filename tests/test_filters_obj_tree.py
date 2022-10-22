import pytest

from query_filter import (q, q_contains, q_filter, q_is_not_none,
                          q_matches_regex)


class Node:
    instances = []

    def __init__(self, name, mother=None, father=None):
        self.name = name
        self.mother = mother
        self.father = father
        self.instances.append(self)

    def __repr__(self):
        return (f"Node('{self.name}', mother={repr(self.mother)}, "
                f"father={repr(self.father)})")


@pytest.fixture
def p_grandfather():
    return Node(name="Wilbur Meadows")


@pytest.fixture
def p_grandmother():
    return Node(name="Halle Meadows (nee Perkins)")


@pytest.fixture
def m_grandfather():
    return Node(name="Jimmy Walsh")


@pytest.fixture
def m_m_ggrandfather():
    return Node(name="Alan Eastwood")


@pytest.fixture
def m_m_ggrandmother():
    return Node(name="Opal Eastwood (nee Plant)")


@pytest.fixture
def m_grandmother(m_m_ggrandmother, m_m_ggrandfather):
    return Node(name="Laura Walsh (nee Stanton)",
                mother=m_m_ggrandmother,
                father=m_m_ggrandfather)


@pytest.fixture
def father(p_grandmother, p_grandfather):
    return Node(name="Isaac Meadows",
                mother=p_grandmother,
                father=p_grandfather)


@pytest.fixture
def mother(m_grandmother, m_grandfather):
    return Node(name="Isobel Meadows (nee Walsh)",
                mother=m_grandmother,
                father=m_grandfather)


@pytest.fixture
def root(mother, father):
    return Node(name="Sally Meadows", mother=mother, father=father)


@pytest.fixture
def all_nodes(root, mother, father,
              m_grandmother, m_grandfather,
              m_m_ggrandmother, m_m_ggrandfather,
              p_grandmother, p_grandfather):
    return [
        root,
        mother,
        father,
        m_grandmother,
        m_grandfather,
        m_m_ggrandmother,
        m_m_ggrandfather,
        p_grandmother,
        p_grandfather
    ]


def test_filter_root_by_furthest_ancestor(all_nodes, root):
    expected = [root]

    results = q_filter(
        all_nodes,
        q_contains(q.mother.mother.mother.name, "Opal Eastwood")
    )

    assert list(results) == expected


def test_filter_root_by_ancestor_kwargs(all_nodes, root):
    expected = [root]

    results = q_filter(
        all_nodes,
        q.mother.mother.name == "Laura Walsh (nee Stanton)"
    )

    assert list(results) == expected


def test_born_walsh_with_father_node(all_nodes, mother):
    expected = [mother]

    results = q_filter(all_nodes,
                       q_matches_regex(q.name, r"Walsh(?! \(nee)"),
                       q_is_not_none(q.father))

    assert list(results) == expected
