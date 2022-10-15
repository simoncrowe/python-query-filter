from datetime import datetime

import pytest

from query_filter import q, q_all, q_any, q_filter, q_not


@pytest.fixture
def version_one():
    return {
        "CreateTime": datetime(2017, 11, 20, 12, 52, 33),
        "DefaultVersion": True,
        "LaunchTemplateData": {
            "ImageId": "ami-aabbcc11",
            "KeyName": "kp-us-east",
            "NetworkInterfaces": [
                {
                    "AssociatePublicIpAddress": True,
                    "DeleteOnTermination": False,
                    "DeviceIndex": 0,
                    "Groups": [
                        "sg-7c227019",
                    ],
                    "SubnetId": "subnet-7b16de0c",
                    "PrivateIpAddress": "80.141.44.12",
                },
            ],
            "UserData": "",
        },
        "CreditSpecification": {
            "CpuCredits": "standard",
        },
        "CpuOptions": {
            "CoreCount": 1,
            "ThreadsPerCore": 2
        },
        "LaunchTemplateId": "lt-068f72b72934aff71",
        "VersionNumber": 1,
    }


@pytest.fixture
def version_two():
    return {
        "CreateTime": datetime(2017, 11, 20, 13, 12, 32),
        "DefaultVersion": False,
        "LaunchTemplateData": {
            "ImageId": "ami-6057e21a",
            "KeyName": "kp-us-east",
            "NetworkInterfaces": [
                {
                    "DeviceIndex": 0,
                    "Groups": [
                        "sg-7c227019",
                    ],
                    "SubnetId": "subnet-db7ea2c5",
                    "PrivateIpAddress": "80.141.44.57",
                },
            ],
        },
        "CreditSpecification": {
            "CpuCredits": "standard",
        },
        "CpuOptions": {
            "CoreCount": 2,
            "ThreadsPerCore": 2
        },
        "LaunchTemplateId": "lt-068f72b72934aff71",
        "VersionNumber": 2,
    }


@pytest.fixture
def version_three():
    return {
        "CreateTime": datetime(2017, 11, 20, 15, 0, 2),
        "DefaultVersion": False,
        "LaunchTemplateData": {
            "ImageId": "ami-2661cf7b",
            "KeyName": "kp-us-east",
            "NetworkInterfaces": [
                {
                    "DeviceIndex": 0,
                    "Groups": [
                        "sg-7c227019",
                    ],
                    "SubnetId": "subnet-a4579fe6",
                    "Ipv6Addresses": [
                        {"Ipv6Address":
                            "2004:90aa:3c4c:c973:a318:af08:58a0:997c"},
                        {"Ipv6Address":
                            "b635:26ad:8fdf:a274:88dc:cf8c:47df:26b7"},
                    ],
                    "Ipv6AddressCount": 2,
                    "PrivateIpAddress": "80.141.152.44",

                },
            ],
        },
        "CpuOptions": {
            "CoreCount": 3,
            "ThreadsPerCore": 1
        },
        "CreditSpecification": {
            "CpuCredits": "standard",
        },
        "LaunchTemplateId": "lt-068f72b72934aff71",
        "VersionNumber": 3
    }


@pytest.fixture
def version_four():
    return {
        "CreateTime": datetime(2017, 11, 20, 15, 45, 33),
        "DefaultVersion": False,
        "LaunchTemplateData": {
            "ImageId": "ami-cc3e8abf",
            "KeyName": "kp-us-east",
            "NetworkInterfaces": [
                {
                    "DeviceIndex": 0,
                    "Groups": [
                        "sg-7c227019",
                    ],
                    "SubnetId": "subnet-a4579fe6",
                    "Ipv6Addresses": [
                        {"Ipv6Address":
                            "4f08:ea60:17f9:3e89:4d66:2e8c:259c:d1a9"},
                        {"Ipv6Address":
                            "b635:26ad:8fdf:a274:88dc:cf8c:47df:26b7"},
                        {"Ipv6Address":
                            "eb7a:5a31:f899:dd8c:e566:3307:a45e:dcf6"},
                    ],
                    "Ipv6AddressCount": 3,
                    "PrivateIpAddress": "80.141.152.14",


                },
            ],
        },
        "CpuOptions": {
            "CoreCount": 4,
            "ThreadsPerCore": 1,
        },
        "CreditSpecification": {
            "CpuCredits": "unlimited",
        },
        "LaunchTemplateId": "lt-aaa68831cce2a8d91",
        "VersionNumber": 4
    }


@pytest.fixture
def version_five():
    return {
        "CreateTime": datetime(2017, 11, 20, 19, 4, 54),
        "DefaultVersion": False,
        "LaunchTemplateData": {
            "ImageId": "ami-2f7ac02a",
            "KeyName": "kp-us-east",
            "NetworkInterfaces": [
                {
                    "DeviceIndex": 0,
                    "Groups": [
                        "sg-1c628b25",
                    ],
                    "SubnetId": "subnet-a4579fe6",
                    "Ipv6Addresses": [
                        {"Ipv6Address":
                            "f486:915c:2be9:b0da:7d60:3fae:d65a:e8d8"},
                        {"Ipv6Address":
                            "eb7a:5a31:f899:dd8c:e566:3307:a45e:dcf6"},
                    ],
                    "Ipv6AddressCount": 2,
                    "PrivateIpAddress": "80.141.152.136",
                },
            ],
        },
        "CpuOptions": {
            "CoreCount": 3,
            "ThreadsPerCore": 2,
        },
        "CreditSpecification": {
            "CpuCredits": "standard",
        },
        "LaunchTemplateId": "lt-aaa68831cce2a8d91",
        "VersionNumber": 5
    }


@pytest.fixture
def all_versions(version_one, version_two, version_three,
                 version_four, version_five):
    return {
        "LaunchTemplateVersions": [
            version_one, version_two, version_three, version_four, version_five
        ],
        "ResponseMetadata": {
            "RequestId": "856F4F9E52336fA4",
            "HostId": "118e71806df8f025567be1b09c071e900",
            "HTTPStatusCode": 200,
            "RetryAttempts": 0
        }
    }


def test_filter_kwarg(all_versions, version_one):
    expected = [version_one]

    results = q_filter(
        all_versions["LaunchTemplateVersions"],
        q["LaunchTemplateData"]["NetworkInterfaces"][0]["AssociatePublicIpAddress"].is_true()
    )

    assert list(results) == expected


def test_filter_non_default_by_group(all_versions, version_two,
                                     version_three, version_four):

    expected = [version_two, version_three, version_four]

    results = q_filter(
        all_versions["LaunchTemplateVersions"],
        q["LaunchTemplateData"]["NetworkInterfaces"][0]["Groups"].contains("sg-7c227019"),
        q["DefaultVersion"].is_false()
    )

    assert list(results) == expected


def test_filter_ip_addresses(all_versions, version_five):
    expected = [version_five]

    results = q_filter(
        all_versions["LaunchTemplateVersions"],
        q["LaunchTemplateData"]["NetworkInterfaces"][0]["Ipv6Addresses"].contains(
            {"Ipv6Address": "eb7a:5a31:f899:dd8c:e566:3307:a45e:dcf6"}
        ),
        q_not(
            q["LaunchTemplateData"]["NetworkInterfaces"][0]["PrivateIpAddress"]
            == "80.141.152.14"
        )
    )

    assert list(results) == expected


def threads_gte(min_threads: int):
    def pred(version: dict):
        cores = version["CpuOptions"]["CoreCount"]
        threads = version["CpuOptions"]["ThreadsPerCore"]
        return cores * threads >= min_threads

    return pred


def test_filter_by_date_and_number_of_threads_custom_pred(all_versions,
                                                          version_two):
    expected = [version_two]

    results = q_filter(all_versions["LaunchTemplateVersions"],
                       threads_gte(4),
                       q["CreateTime"] < datetime(2017, 11, 20, 15, 40))

    assert list(results) == expected


def test_filter_all_cpu_thread_or_credits(all_versions, version_two,
                                          version_four, version_five):
    expected = [version_four]

    results = q_filter(
        all_versions["LaunchTemplateVersions"],
        q_all(
            threads_gte(4),
            q["CreditSpecification"]["CpuCredits"] == "unlimited"
        )
    )

    assert list(results) == expected


def test_filter_not_all_cpu_thread_or_credits(all_versions, version_one,
                                              version_two, version_three,
                                              version_five):
    expected = [version_one, version_two, version_three, version_five]

    results = q_filter(
        all_versions["LaunchTemplateVersions"],
        q_not(
            q_all(
                threads_gte(4),
                q["CreditSpecification"]["CpuCredits"] == "unlimited"
            )
        )
    )

    assert list(results) == expected


def test_filter_any_cpu_thread_or_credits(all_versions, version_two,
                                          version_four, version_five):
    expected = [version_two, version_four, version_five]

    results = q_filter(
        all_versions["LaunchTemplateVersions"],
        q_any(
            threads_gte(4),
            q["CreditSpecification"]["CpuCredits"] == "unlimited"
        )
    )

    assert list(results) == expected


def test_filter_not_any_cpu_thread_or_credits(all_versions, version_one,
                                              version_three):
    expected = [version_one, version_three]

    results = q_filter(
        all_versions["LaunchTemplateVersions"],
        q_not(
            q_any(
                threads_gte(4),
                q["CreditSpecification"]["CpuCredits"] == "unlimited"
            )
        )
    )

    assert list(results) == expected
