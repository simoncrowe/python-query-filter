## python-query-filter

This package provides a function-based API for filtering collections of
heterogeneous, nested dictionaries or complex objects. It has 100% test
coverage.

At the core of the API is the `q_filter` function, which is like
the built-in `filter` function, but take any number of predicate functions
rather than just one.

The remainder of the functions in this package
are used to construct predicates that evaluate items
or attributes within filtered objects.

Inspired by the more class-based [QueryableList](https://github.com/kata198/QueryableList).

### Use Case
This package is best suited to nested, heterogeneous data that
one might find in a serialised HTTP response body.

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
>>> from query_filter import q_filter, q
>>> results = q_filter(
        versions_data["LaunchTemplateVersions"],
        q["LaunchTemplateData"]["NetworkInterfaces"][0]["AssociatePublicIpAddress"]
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

The filter above doesn't use `== True` but rather checks
the truthiness of the `"AssociatePublicIpAddress"` key's value.

The equivalent generator expression for a simple query likes this
is less readable.

```python
>>> from typing import Collection
>>> results = (
        version for version in versions_data["LaunchTemplateVersions"]
        if version.get("LaunchTemplateData", {}).get("NetworkInterfaces") and
        isinstance(version["LaunchTemplateData"]["NetworkInterfaces"], Collection) and
        version["LaunchTemplateData"]["NetworkInterfaces"][0].get("AssociatePublicIpAddress")
    )
```

This example is excessively defensive, but hopefully it explains the motivation
behind this tool.

A  `get` call is needed in the generator expression above because the item
`"AssociatePublicIpAddress"` is sometimes missing.
The first two conditions aren't strictly needed to filter the example data.
However, they do illustrate the fact that `q_item` predicates silently
return false if `"LaunchTemplateData"` is not present, or
if `"NetworkInterfaces"` is missing, is not a collection
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
>>> from query_filter import q, q_any, q_filter
>>> results = q_filter(
        versions_data["LaunchTemplateVersions"],
        q_any(
            threads_gte(5),
            q["CreditSpecification"]["CpuCredits"] == "unlimited"
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
>>> from query_filter import q, q_contains, q_filter
>>> results = q_filter(
        Node.instances,
        q_contains(q.mother.mother.mother.name, "Opal Eastwood")
    )
>>> list(results)
[Node('Tiya Meadows', mother=Node('Isobel Meadows (nee Walsh)', mother=Node('Laura Walsh (nee Stanton)', mother=Node('Opal Eastwood (nee Plant)', mother=None, father=None), father=Node('Alan Eastwood', mother=None, father=None)), father=Node('Jimmy Walsh', mother=None, father=None)), father=Node('Isaac Meadows', mother=Node('Halle Meadows (nee Perkins)', mother=None, father=None), father=Node('Wilbur Meadows', mother=None, father=None)))]
```

`q_contains` above is the equivalent of the expression:
`"Opal Eastwood" in Node.instances.mother.mother.mother.name`.
It is one of several functions that enable us to create queries
based on operators that cannot be overloaded in the same way
as the comparison operators.

Here is another example:

```python
>>> from query_filter import q, q_is_not, q_matches_regex, q_filter
>>> results = q_filter(Node.instances,
                       q_matches_regex(q.name, r"Walsh(?! \(nee)"),
                       q_is_not(q.father, None))
>>> list(results)
[Node('Isobel Meadows (nee Walsh)', mother=Node('Laura Walsh (nee Stanton)', mother=Node('Opal Eastwood (nee Plant)', mother=None, father=None), father=Node('Alan Eastwood', mother=None, father=None)), father=Node('Jimmy Walsh', mother=None, father=None))]
```

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

#### Building Queries
The `Query` class, an instance of which is always imported as `q`
is used to specify attribute and item access.

##### Operators
The class supports some operators which offer the most convenient API
for building queries.

###### Comparison

The `Query` class supports all six comparison operators:
`<`, `<=`, `==`, `!=`, `>` and `>=`.

###### Bitwise
The bitwise not operator `~` negates the truthiness of the `Query` object.

For example `q.is_active` will produce a predicate that returns `True` if
an object has an attributes named `is_active` and that attribute's value
is truthy.

`~q.is_active` will produce the opposite result.

#####  Functions
There are some useful operators such as `is` that cannot be overloaded.
Most of the functions below replace these.

##### query\_filter.q\_is\_in(query: Query, container: Container) -> Callable[[Any], bool]
Returns a predicate that's true if the queried object is the `container` argument.

##### query\_filter.q\_contains(query: Query, member: Any) -> Callable[[Container], bool]
Returns a predicate that's true if the queried object contains the `member` argument.

##### query\_filter.q\_is(query: Query, criterion: Any) -> Callable[[Any], bool]
Returns a predicate that's true if the queried object is identical
to the criterion object.

##### query\_filter.q\_is\_not(query, criterion: Any) -> Callable[[Any], bool]
Returns a predicate that's true if the queried object is not identical
to the criterion object.

##### query\_filter.q\_matches\_regex(query: Query, pattern: str | bytes) -> [[str | bytes], bool]
This function may be convenient when working with strings and byte strings.
It returns a predicate that's true if the queried object matches the regular expression
`pattern` argument.

### Tests

If you want to run tests, you'll first need to install the package
from source and make it editable. Ensuring that you're in the root directory
of this repo, enter:

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
- Query all items in an iterable rather than just one using `...`
- Build queries out of `Query` objects using the `&` and `|` operators
