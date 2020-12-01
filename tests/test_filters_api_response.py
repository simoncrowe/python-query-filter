from datetime import datetime

import pytest

from query_filter import (
    k_attrs,
    k_items,
    q_all,
    q_any,
    q_attr,
    q_filter,
    q_item,
    q_not,
)

# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.describe_launch_template_versions


@pytest.fixture
def version_one():
    return {
        'CreateTime': datetime(2017, 11, 20, 12, 52, 33),
        'CreatedBy': 'arn:aws:iam::123456789102:root',
        'DefaultVersion': True,
        'LaunchTemplateData': {
            'ImageId': 'ami-aabbcc11',
            'InstanceType': 't2.medium',
            'KeyName': 'kp-us-east',
            'NetworkInterfaces': [
                {
                    'AssociatePublicIpAddress': True,
                    'DeleteOnTermination': False,
                    'DeviceIndex': 0,
                    'Groups': [
                        'sg-7c227019',
                    ],
                    'SubnetId': 'subnet-7b16de0c',
                },
            ],
            'UserData': '',
        },
        'LaunchTemplateId': 'lt-068f72b72934aff71',
        'LaunchTemplateName': 'Webservers',
        'VersionNumber': 1,
    }


@pytest.fixture
def version_two():
    return {
        'CreateTime': datetime(2017, 11, 20, 13, 12, 32),
        'CreatedBy': 'arn:aws:iam::123456789102:root',
        'DefaultVersion': False,
        'LaunchTemplateData': {
            'ImageId': 'ami-6057e21a',
            'InstanceType': 't2.medium',
            'KeyName': 'kp-us-east',
            'NetworkInterfaces': [
                {
                    'DeviceIndex': 0,
                    'Groups': [
                        'sg-7c227019',
                    ],
                    'SubnetId': 'subnet-1a2b3c4d',
                },
            ],
        },
        'LaunchTemplateId': 'lt-068f72b72934aff71',
        'LaunchTemplateName': 'Webservers',
        'VersionNumber': 2,
    }
