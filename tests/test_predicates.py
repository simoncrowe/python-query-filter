import pytest

from query_filter.predicates import retrieve_attr, retrieve_item


class Node:

    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None
    

@pytest.fixture
def root_node(left_node, right_node):
    root = Node(0)
    root.left = left_node
    root.right = right_node
    return root


@pytest.fixture
def left_node():
    return Node(1)


@pytest.fixture
def right_node(right_right_node):
    right =  Node(2)
    right.right = right_right_node
    return right


@pytest.fixture
def right_right_node():
    return Node(3)

def test_retrieve_attr_single_key(root_node):
    result = retrieve_attr(root_node, ("data",))
    assert result == root_node.data


def test_retrieve_attr_two_keys(root_node, left_node):
    result = retrieve_attr(root_node, ("left", "data"))
    assert result == left_node.data


def test_retrieve_attr_three_keys(root_node, right_right_node):
    result = retrieve_attr(root_node, ("right", "right", "data"))
    assert result == right_right_node.data


def test_retrieve_atte_three_keys_to_nonexistant_attr(root_node):
    result = retrieve_attr(root_node , ("left", "left", "data"))
    assert result == None

