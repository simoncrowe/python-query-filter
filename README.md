# python-query-filter

This package provides a functional API for filtering collections of
heterogeneous, nested dictionaries or complex objects.

At the core of this API are `q_filter` functions, which are like
the built-in `filter` function, but take any number of predicate functions
rather than just one.

The remainder of the functions in this package
are used to construct predicates that evaluate items
or attributes within filtered objects.

## Use Case
This package is best suited to nested, heterogenous data. Collections
of flat homogenous dictionaries or objects are easier to filter with
list comprehensions or generator expressions.

### Examples
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
#### Filtering by list/dictionary items
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

One reason for this is that the item `"AssociatePublicIpAddress"` is always
present. The predicate returned by `is_true` above will silently return `False`
on missing keys, whereas with the generator expression we need to call `get`
to avoid a `KeyError`. We're not even considering the case of an empty
list for `"NetworkInterfaces"` here.

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
