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
This package is best suited to nested, heterogenous data. Collections
of flat homogenous dictionaries or objects are easier to filter with
list comprehensions or generator expressions.

### Examples

#### Filtering by list/dictionary items
In these example we'll be filtering a typtical response from `boto3`,
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
        data["LaunchTemplateVersions"],
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

The eqivelant generator expression for a simple query likes this
is (in my admittedly biased oppinion) a little less readible.

```python
>>> results = (
        version for version in data["LaunchTemplateVersions"]
        if version["LaunchTemplateData"]["NetworkInterfaces"][0].get("AssociatePublicIpAddress") is True
    )
```

One reason for this is that the item `"AssociatePublicIpAddress"` is sometimes
missing. The predicate returned by `is_true` above will silently return `False`
on missing keys, whereas with the generator expression we need to call `get`
to avoid a `KeyError`. This doesn't even take into account the possibility of
an empty list for `"NetworkInterfaces"` here.

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

Here we're using `q_any`, which combines the predicates passsed into it,
returning `True` if at least one of them is satisfied.

```python
>>> from query_filter import q_any, q_filter, q_item
>>> results = q_filter(
        data["LaunchTemplateVersions"],
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

To demonstate the syntax, we can filter for the root node by their
great-great grandmother.

```python
>>> results = q_filter(
        Node.instances,
        q_attr("mother.mother.mother.name").contains("Opal Eastwood")
    )
>>> list(results)
[Node('Tiya Meadows', mother=Node('Isobel Meadows (nee Walsh)', mother=Node('Laura Walsh (nee Stanton)', mother=Node('Opal Eastwood (nee Plant)', mother=None, father=None), father=Node('Alan Eastwood', mother=None, father=None)), father=Node('Jimmy Walsh', mother=None, father=None)), father=Node('Isaac Meadows', mother=Node('Halle Meadows (nee Perkins)', mother=None, father=None), father=Node('Wilbur Meadows', mother=None, father=None)))]
```

As attribures names can only be alphabetic characters and underscores,
it make sense to separate them with dots.


#### Using Django-style keyword arguments

If you want to filter based on multiple attributes, you can pass the paths
as keyword arguments to the `k_attrs` function. This query looks for nodes
born with the surname Walsh that have a father node.

```python
>>> from query_filter import k_attrs, q_filter
>>> results = q_filter(Node.instances,
                       k_attrs(name__regex=r"Walsh(?! \(nee)",
                               father__is_not=None))
>>> list(results)
[Node('Isobel Meadows (nee Walsh)', mother=Node('Laura Walsh (nee Stanton)', mother=Node('Opal Eastwood (nee Plant)', mother=None, father=None), father=Node('Alan Eastwood', mother=None, father=None)), father=Node('Jimmy Walsh', mother=None, father=None))]

```

NOTE: There is also a `k_items` function that can be used to filter dictinaries.
It only works with string keys. You can include special characters and spaces
 by using `**`:
```python
k_items(**{"Cr4zy K3y!__ne": "sane"})
```

This restriction to strings is quite a limitation, considering that a dictionary
key can be any hashable object. `k_items` also cannot filter lists or similar objects
as it doesn't cast the double-underscore-delimited strings to integers.

### API

#### Filter functions

##### `query_filter.q_filter`
This is an alias for `query_filter.q_filter_all`

#####

#### query functions

### Tests

If you want to run tests, you'll first need to install the package
from source as editable. Ensuring that you're in the root direcory, of this repo,
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
