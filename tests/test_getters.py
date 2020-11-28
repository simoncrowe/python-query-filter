import pytest

from query_filter.filter import retrieve_attr, retrieve_item


class Node:

    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None

    def as_dict(self):
        return {
            "data": self.data,
            "left": self.left.as_dict() if self.left else None,
            "right": self.right.as_dict() if self.right else None,
        }


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
    right = Node(2)
    right.right = right_right_node
    return right


@pytest.fixture
def right_right_node():
    return Node(3)


@pytest.fixture
def tree_dict(root_node):
    return root_node.as_dict()


def test_retrieve_attr_single_key(root_node):
    result = retrieve_attr(root_node, "data")
    assert result == root_node.data


def test_retrieve_attr_two_keys(root_node, left_node):
    result = retrieve_attr(root_node, "left", "data")
    assert result == left_node.data


def test_retrieve_attr_three_keys(root_node, right_right_node):
    result = retrieve_attr(root_node, "right", "right", "data")
    assert result == right_right_node.data


def test_retrieve_attr_three_keys_to_nonexistant_attr(root_node):
    result = retrieve_attr(root_node, "left", "left", "data")
    assert result is None


def test_retrieve_item_single_key(tree_dict, root_node):
    result = retrieve_item(tree_dict, "data")
    assert result == root_node.data


def test_retrieve_item_two_keys(tree_dict, left_node):
    result = retrieve_item(tree_dict, "left", "data")
    assert result == left_node.data


def test_retrieve_item_three_keys(tree_dict, right_right_node):
    result = retrieve_item(tree_dict, "right", "right", "data")
    assert result == right_right_node.data


def test_retrieve_item_three_keys_to_nonexistant_item(tree_dict):
    result = retrieve_item(tree_dict, "left", "left", "data")
    assert result is None


def test_retrive_item_index():
    items = ["zero", "one", "two", "tree"]
    result = retrieve_item(items, 1)
    assert result == "one"


def test_retrive_item_index_out_of_range():
    items = ["zero", "one", "two", "tree"]
    result = retrieve_item(items, 9)
    assert result is None
