## python-query-filter

This package provides a functional API for filtering collections of
heterogeneous, nested dictionaries or complex objects. It has 100% test
coverage.

At the core of this API are `q_filter` functions, which are like
the built-in `filter` function, but take any number of predicate functions
rather than just one.

The remainder of the functions in this package
are used to construct predicates that evaluate items
or attributes within filtered objects.

### Use Case
This package is best suited to nested, heterogeneous data. Collections
of flat, homogeneous dictionaries or objects are easier to filter with
list comprehensions or generator expressions.

### Install
```sh
pip install query-filter
```

### Examples

#### Filtering by list/dictionary items
In the next few examples, we'll be filtering a typical response from `boto3`,
the python client for Amazon Web Services.

```python
>>> versions_data
{'LaunchTemplateVersions': [{'CreateTime': datetime.datetime(2017, 11, 20, 12, 52, 33),
   'DefaultVersion': True,
   'LaunchTemplateData': {'ImageId': 'ami-aabbcc11',
    'KeyName': 'kp-us-east',
    'NetworkInterfaces': [{'AssociatePublicIpAddress': True,
      'DeleteOnTermination': False,
      'DeviceIndex': 0,
      'Groups': ['sg-7c227019'],
      'SubnetId': 'subnet-7b16de0c',
      'PrivateIpAddress': '80.141.44.12'}],
    'UserData': ''},
   'CreditSpecification': {'CpuCredits': 'standard'},
   'CpuOptions': {'CoreCount': 1, 'ThreadsPerCore': 2},
   'LaunchTemplateId': 'lt-068f72b72934aff71',
   'VersionNumber': 1},
  {'CreateTime': datetime.datetime(2017, 11, 20, 13, 12, 32),
   'DefaultVersion': False,
   'LaunchTemplateData': {'ImageId': 'ami-6057e21a',
    'KeyName': 'kp-us-east',
    'NetworkInterfaces': [{'DeviceIndex': 0,
      'Groups': ['sg-7c227019'],
      'SubnetId': 'subnet-db7ea2c5',
      'PrivateIpAddress': '80.141.44.57'}]},
   'CreditSpecification': {'CpuCredits': 'standard'},
   'CpuOptions': {'CoreCount': 2, 'ThreadsPerCore': 2},
   'LaunchTemplateId': 'lt-068f72b72934aff71',
   'VersionNumber': 2},
  {'CreateTime': datetime.datetime(2017, 11, 20, 15, 0, 2),
   'DefaultVersion': False,
   'LaunchTemplateData': {'ImageId': 'ami-2661cf7b',
    'KeyName': 'kp-us-east',
    'NetworkInterfaces': [{'DeviceIndex': 0,
      'Groups': ['sg-7c227019'],
      'SubnetId': 'subnet-a4579fe6',
      'Ipv6Addresses': [{'Ipv6Address': '2004:90aa:3c4c:c973:a318:af08:58a0:997c'},
       {'Ipv6Address': 'b635:26ad:8fdf:a274:88dc:cf8c:47df:26b7'}],
      'Ipv6AddressCount': 2,
      'PrivateIpAddress': '80.141.152.44'}]},
   'CpuOptions': {'CoreCount': 3, 'ThreadsPerCore': 1},
   'CreditSpecification': {'CpuCredits': 'standard'},
   'LaunchTemplateId': 'lt-068f72b72934aff71',
   'VersionNumber': 3},
  {'CreateTime': datetime.datetime(2017, 11, 20, 15, 45, 33),
   'DefaultVersion': False,
   'LaunchTemplateData': {'ImageId': 'ami-cc3e8abf',
    'KeyName': 'kp-us-east',
    'NetworkInterfaces': [{'DeviceIndex': 0,
      'Groups': ['sg-7c227019'],
      'SubnetId': 'subnet-a4579fe6',
      'Ipv6Addresses': [{'Ipv6Address': '4f08:ea60:17f9:3e89:4d66:2e8c:259c:d1a9'},
       {'Ipv6Address': 'b635:26ad:8fdf:a274:88dc:cf8c:47df:26b7'},
       {'Ipv6Address': 'eb7a:5a31:f899:dd8c:e566:3307:a45e:dcf6'}],
      'Ipv6AddressCount': 3,
      'PrivateIpAddress': '80.141.152.14'}]},
   'CpuOptions': {'CoreCount': 4, 'ThreadsPerCore': 1},
   'CreditSpecification': {'CpuCredits': 'unlimited'},
   'LaunchTemplateId': 'lt-aaa68831cce2a8d91',
   'VersionNumber': 4},
  {'CreateTime': datetime.datetime(2017, 11, 20, 19, 4, 54),
   'DefaultVersion': False,
   'LaunchTemplateData': {'ImageId': 'ami-2f7ac02a',
    'KeyName': 'kp-us-east',
    'NetworkInterfaces': [{'DeviceIndex': 0,
      'Groups': ['sg-1c628b25'],
      'SubnetId': 'subnet-a4579fe6',
      'Ipv6Addresses': [{'Ipv6Address': 'f486:915c:2be9:b0da:7d60:3fae:d65a:e8d8'},
       {'Ipv6Address': 'eb7a:5a31:f899:dd8c:e566:3307:a45e:dcf6'}],
      'Ipv6AddressCount': 2,
      'PrivateIpAddress': '80.141.152.136'}]},
   'CpuOptions': {'CoreCount': 3, 'ThreadsPerCore': 2},
   'CreditSpecification': {'CpuCredits': 'standard'},
   'LaunchTemplateId': 'lt-aaa68831cce2a8d91',
   'VersionNumber': 5}],
 'ResponseMetadata': {'RequestId': '856F4F9E52336fA4',
  'HostId': '118e71806df8f025567be1b09c071e900',
  'HTTPStatusCode': 200,
  'RetryAttempts': 0}}
```

If we want to get data that have `AssociatePublicIpAddress`
set to `True`, we can do the following:

```python
>>> from query_filter import q_filter, q_item
>>> results = q_filter(
        versions_data["LaunchTemplateVersions"],
        q_item(
            "LaunchTemplateData", "NetworkInterfaces", 0, "AssociatePublicIpAddress"
        ).is_true()
    )
>>> results
<filter at 0x7f3515cba240>
>>> list(results)
[{'CreateTime': datetime.datetime(2017, 11, 20, 12, 52, 33),
  'DefaultVersion': True,
  'LaunchTemplateData': {'ImageId': 'ami-aabbcc11',
   'KeyName': 'kp-us-east',
   'NetworkInterfaces': [{'AssociatePublicIpAddress': True,
     'DeleteOnTermination': False,
     'DeviceIndex': 0,
     'Groups': ['sg-7c227019'],
     'SubnetId': 'subnet-7b16de0c',
     'PrivateIpAddress': '80.141.44.12'}],
   'UserData': ''},
  'CreditSpecification': {'CpuCredits': 'standard'},
  'CpuOptions': {'CoreCount': 1, 'ThreadsPerCore': 2},
  'LaunchTemplateId': 'lt-068f72b72934aff71',
  'VersionNumber': 1}]
```

The equivalent generator expression for a simple query likes this
is less readable.

```python
>>> from typing import Collection
>>> results = (
        version for version in versions_data["LaunchTemplateVersions"]
        if version["LaunchTemplateData"].get("NetworkInterfaces") and
        isinstance(version["LaunchTemplateData"]["NetworkInterfaces"], Collection) and
        version["LaunchTemplateData"]["NetworkInterfaces"][0].get("AssociatePublicIpAddress") is True
    )
```

This example is excessive, but hopefully it explains the motivation
behind this tool.
A `get` call is needed in the generator expression above because the item
`"AssociatePublicIpAddress"` is sometimes missing.
The first two conditions aren't strictly needed to filter the example data.
However, they do illustrate the fact that `q_item` predicates silently
return false if "NetworkInterfaces" is not present, is not a collection
or is an empty collection.

#### Filtering using custom predicates

We can combine custom queries with those created with the help
of this package. The following predicate can be used to ensure
that the launch template versions specify a sufficient number of
threads.

```python
def threads_gte(min_threads: int):
    def pred(version: dict):
        cores = version["CpuOptions"]["CoreCount"]
        threads = version["CpuOptions"]["ThreadsPerCore"]
        return cores * threads >= min_threads

    return pred
```

Here we're using `q_any`, which combines the predicates passed into it,
returning `True` if at least one of them is satisfied.

```python
>>> from query_filter import q_any, q_filter, q_item
>>> results = q_filter(
        versions_data["LaunchTemplateVersions"],
        q_any(
            threads_gte(5),
            q_item("CreditSpecification", "CpuCredits") == "unlimited"
        )
    )
>>> list(results)
[{'CreateTime': datetime.datetime(2017, 11, 20, 15, 45, 33),
  'DefaultVersion': False,
  'LaunchTemplateData': {'ImageId': 'ami-cc3e8abf',
   'KeyName': 'kp-us-east',
   'NetworkInterfaces': [{'DeviceIndex': 0,
     'Groups': ['sg-7c227019'],
     'SubnetId': 'subnet-a4579fe6',
     'Ipv6Addresses': [{'Ipv6Address': '4f08:ea60:17f9:3e89:4d66:2e8c:259c:d1a9'},
      {'Ipv6Address': 'b635:26ad:8fdf:a274:88dc:cf8c:47df:26b7'},
      {'Ipv6Address': 'eb7a:5a31:f899:dd8c:e566:3307:a45e:dcf6'}],
     'Ipv6AddressCount': 3,
     'PrivateIpAddress': '80.141.152.14'}]},
  'CpuOptions': {'CoreCount': 4, 'ThreadsPerCore': 1},
  'CreditSpecification': {'CpuCredits': 'unlimited'},
  'LaunchTemplateId': 'lt-aaa68831cce2a8d91',
  'VersionNumber': 4},
 {'CreateTime': datetime.datetime(2017, 11, 20, 19, 4, 54),
  'DefaultVersion': False,
  'LaunchTemplateData': {'ImageId': 'ami-2f7ac02a',
   'KeyName': 'kp-us-east',
   'NetworkInterfaces': [{'DeviceIndex': 0,
     'Groups': ['sg-1c628b25'],
     'SubnetId': 'subnet-a4579fe6',
     'Ipv6Addresses': [{'Ipv6Address': 'f486:915c:2be9:b0da:7d60:3fae:d65a:e8d8'},
      {'Ipv6Address': 'eb7a:5a31:f899:dd8c:e566:3307:a45e:dcf6'}],
     'Ipv6AddressCount': 2,
     'PrivateIpAddress': '80.141.152.136'}]},
  'CpuOptions': {'CoreCount': 3, 'ThreadsPerCore': 2},
  'CreditSpecification': {'CpuCredits': 'standard'},
  'LaunchTemplateId': 'lt-aaa68831cce2a8d91',
  'VersionNumber': 5}]
```

#### Filtering by object attributes

This can be useful if you're working with objects that have a lot
of "has-a" relationships to other objects. For brevity,
a hacky binary tree-like class is used to build a fictional ancestor chart.

```python
>>> class Node:
    instances = []
    def __init__(self, name, mother=None, father=None):
        self.name = name
        self.mother = mother
        self.father = father
        self.instances.append(self)
    def __repr__(self):
        return (f"Node('{self.name}', mother={repr(self.mother)}, "
                f"father={repr(self.father)})")
>>> Node(name='Tiya Meadows',
         mother=Node('Isobel Meadows (nee Walsh)',
                     mother=Node(name='Laura Walsh (nee Stanton)',
                                 mother=Node('Opal Eastwood (nee Plant)'),
                                 father=Node('Alan Eastwood')),
                     father=Node(name='Jimmy Walsh')),
         father=Node(name='Isaac Meadows',
                     mother=Node('Halle Meadows (nee Perkins)'),
                     father=Node('Wilbur Meadows')))
```

To demonstrate the syntax, we can filter for the root node by their
great-great-grandmother.

```python
>>> results = q_filter(
        Node.instances,
        q_attr("mother.mother.mother.name").contains("Opal Eastwood")
    )
>>> list(results)
[Node('Tiya Meadows', mother=Node('Isobel Meadows (nee Walsh)', mother=Node('Laura Walsh (nee Stanton)', mother=Node('Opal Eastwood (nee Plant)', mother=None, father=None), father=Node('Alan Eastwood', mother=None, father=None)), father=Node('Jimmy Walsh', mother=None, father=None)), father=Node('Isaac Meadows', mother=Node('Halle Meadows (nee Perkins)', mother=None, father=None), father=Node('Wilbur Meadows', mother=None, father=None)))]
```

As attribute names can only be alphabetic characters and underscores*,
it makes sense to separate them with dots.

*It is technically possible to use other characters
when calling `setattr` or mutating an object's `__dict__` attribute.
However, names containing these characters don't work
with python's normal syntax for attribute access
so they aren't taken into consideration.

#### Using Django-style keyword arguments

If you want to filter based on multiple attributes, you can pass the paths
as keyword arguments to the `q_attrs` function. This query looks for nodes
born with the surname Walsh that have a father node.

```python
>>> from query_filter import q_attrs, q_filter
>>> results = q_filter(Node.instances,
                       q_attrs(name__regex=r"Walsh(?! \(nee)",
                               father__is_not=None))
>>> list(results)
[Node('Isobel Meadows (nee Walsh)', mother=Node('Laura Walsh (nee Stanton)', mother=Node('Opal Eastwood (nee Plant)', mother=None, father=None), father=Node('Alan Eastwood', mother=None, father=None)), father=Node('Jimmy Walsh', mother=None, father=None))]

```

NOTE: There is also a `q_items` function that can be used to filter dictionaries.
It only works with string keys. You can include special characters and spaces
 by using `**`:
```python
q_items(**{"Cr4zy K3y!__ne": "sane"})
```

This restriction to strings is quite a limitation, considering that a dictionary
key can be any hashable object. `q_items` also cannot filter lists or similar objects
as it doesn't cast the double-underscore-delimited strings to integers.

### API

#### Filter functions

##### query\_filter.q\_filter
This is an alias for `query_filter.q_filter_all`.

##### query\_filter.q\_filter\_all(objects: Iterable, *preds, copy=True) -> Iterable[Any]
Returns objects for which all of the predicates in `preds` are true.

##### query\_filter.q\_filter\_any(objects: Iterable, *preds) -> Iterable[Any]
Returns objects for which any of the predicates in `preds` are true.

##### query\_filter.q\_filter\_not\_any(objects: Iterable, *preds) -> Iterable[Any]
Returns objects for which none of the predicates in `preds` is true.

##### query\_filter.q\_all(*preds: Callable) -> Callable
Returns a predicate that returns `True` if all predicates
in `preds` return `True`.

##### query\_filter.q\_any(*preds: Callable) -> Callable
Returns a predicate that returns `True` if any predicates
in `preds` return `True`.

##### query\_filter.q\_not(pred: Callable) -> Callable
Returns a predicate that returns `True` if the predicate `pred` returns `False`.

#### query functions
##### query\_filter.q\_attr(path: str) -> Query
Returns a `Query` object for evaluating attributes
indicated by the dot-delimited `path` argument.

Query instances expose methods (magic and otherwise)
for comparison etc. These methods return predicates.

##### query\_filter.q\_attrs
This is an alias of `query_filter.q_attrs_all`.

##### query\_filter.q\_attrs\_all(\*\*kwargs) -> Callable
Returns a predicate that evaluates an object based on one or more filters.
These filters are defined using keyword arguments in a similar way
to Django's `filter` function.
What attribute to filter is indicated in the first part of the key,
as a double-underscore-delimited path. How to filter
is indicated by the last part of the key. The value is the criterion
against which to filter.

See the **"q_*s" plural predicate keyword arguemts** section below
for information on valid keyword arguments.

##### query\_filter.q\_attrs\_any(\*\*kwargs) -> Callable
Like `q_attrs_all` but returns `True` if _any_ query evaluates `True`.

##### query\_filter.q\_attrs\_not\_any(\*\*kwargs) -> Callable
Like `q_attrs_all` but returns `True` if _no_ queries evaluate `True`.

##### query\_filter.q\_item(\*keys: Hashable) -> Query
Returns a `Query` object for evaluating items
indicated by one or more keys, passed as positional arguments.

##### query\_filter.q\_items
This is an alias of `query_filter.q_items_all`.

##### query\_filter.q\_items\_all(\*\*kwargs) -> Callable
Like `q_attrs_all`, but for items, such as those in a dictionary.

##### query\_filter.q\_items\_any(\*\*kwargs) -> Callable
Like `q_items_all` but returns `True` if _any_ query evaluates `True`.

##### query\_filter.q\_items\_not\_any(\*\*kwargs) -> Callable
Like `q_items_all` but returns `True` if _no_ queries evaluate `True`.

##### query\_filter.q\_items
This is an alias of `query_filter.q_items_all`.


#### Query methods
The `Query` class behaves a bit like a Pandas Series, in that
it supports comparisons using equality operators as well as method calls.
It has the following methods for creating predicates.

##### Query.lt(self, criteria: Any) -> Callable
Returns a predicate that's true if the queried object is less than the criterion.

##### Query.\_\_lt\_\_(self, criterion: Any) -> Callable
Same as `Query.lt`. Call using the `<` operator.

##### Query.lte(self, criterion: Any) -> Callable
Returns a predicate that's true
if the queried object is less than or equal to the criterion.

##### Query.\_\_le\_\_(self, criterion: Any) -> Callable
Same as `Query.lte`. Call using the`<=` operator.

##### Query.eq(self, criterion: Any) -> Callable
Returns a predicate that's true if the queried object is equal to the criterion.

##### Query.\_\_eq\_\_(self, criterion: Any) -> Callable
Same as `Query.eq`, Call using the `==` operator.

##### Query.ne(self, criterion: Any) -> Callable
Returns a predicate that's true if the queried object is not equal to the criterion.

##### Query.\_\_ne\_\_(self, criterion: Any) -> Callable
Same as `Query.ne`, Call using the `!=` operator.

##### Query.gt(self, criterion: Any) -> Callable
Returns a predicate that's true if the queried object is greater than the criterion.

##### Query.\_\_gt\_\_(self, criterion: Any) -> Callable
Same as `Query.gt`, Call using the `>` operator.

##### Query.gte(self, criterion: Any) -> Callable
Returns a predicate that's true if the queried object is greater than or equal to the criterion.

##### Query.\_\_ge\_\_(self, criterion: Any) -> Callable
Same as `Query.gte`, Call using the `>=` operator.

##### Query.is\_in(self, container: Any) -> Callable
Returns a predicate that's true if the queried object is the `container` argument.

##### Query.contains(self, member: Any) -> Callable
Returns a predicate that's true if the queried object contains the `member` argument.

##### Query.regex(self, pattern: str) -> Callable
Returns a predicate that's true if the queried object matches the regular expression
`pattern` argument. This only works for strings and byte strings.

##### Query.is\_none(self) -> Callable
Returns a predicate that's true if the queried object is `None`.

##### Query.is\_not\_none(self) -> Callable
Returns a predicate that's true if the queried object is not `None`.

##### Query.is\_true(self) -> Callable
Returns a predicate that's true if the queried object is `True`.

##### Query.is\_false(self) -> Callable
Returns a predicate that's true if the queried object is `False`.

#### "q_*s" plural predicate keyword arguemts
Attribute names, keys and query names are separated by double-underscores. e.q `__`.

The general form is simlar to the what's used in Django:
`(parent_attr__child_attr__query_name="Criteria for query")`.
If the query name at the end is ommited, equality is assumed.
`(parent_attr__child_attr=42)` is equivalent to `(parent_attr__child_attr__eq=42)`.

These are the supported query names:
 - `lt`: less than the specified criteria
 - `lte`: less than or equal to the specified criteria
 - `eq`: equal to the specified criteria
 - `ne`: not equal to the specified criteria
 - `gt`: greater than the specified criteria
 - `gte`: greater than or equal to the specified criteria
 - `in`: the specified criteria contains the queried object
 - `contains`: the queried object contains the specified criteria
 - `regex`:  the queried object contains at least one match for the specified regular expression. This only works for strings and byte strings.
 - `is`: the queried object is identical to the specified criteria
 - `is_not`: the queried object is not identical to the specified criteria

### Tests

If you want to run tests, you'll first need to install the package
from source and make it editable. Ensuring that you're in the root directory, of this repo,
enter:

```sh
pip install -e .
pip install -r requirements/development.txt
pytest
```

To run tests with coverage:

```sh
coverage run  --source "query_filter" -m pytest tests
coverage report
```

### Feature ideas
- Query all items in an iterable rather than just one
  (when that's even possible).
