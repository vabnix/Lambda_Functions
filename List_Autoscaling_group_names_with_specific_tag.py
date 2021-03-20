# Approach 1

import boto3

client = boto3.client('autoscaling')
paginator = client.get_paginator('describe_auto_scaling_groups')
page_iterator = paginator.paginate(
    PaginationConfig={'PageSize': 100}
)

filtered_asgs = page_iterator.search(
    'AutoScalingGroups[] | [?contains(Tags[?Key==`{}`].Value, `{}`)]'.format(
        'Application', 'CCP')
)

for asg in filtered_asgs:
    print
    asg['AutoScalingGroupName']


# Approach 2

def get_asg_name_from_tags(tags):
    asg_name = None
    client = boto3.client('autoscaling')
    while True:

        paginator = client.get_paginator('describe_auto_scaling_groups')
        page_iterator = paginator.paginate(
            PaginationConfig={'PageSize': 100}
        )
        filter = 'AutoScalingGroups[]'
        for tag in tags:
            filter = ('{} | [?contains(Tags[?Key==`{}`].Value, `{}`)]'.format(filter, tag, tags[tag]))
        filtered_asgs = page_iterator.search(filter)
        asg = filtered_asgs.next()
        asg_name = asg['AutoScalingGroupName']
        try:
            asgX = filtered_asgs.next()
            asgX_name = asg['AutoScalingGroupName']
            raise AssertionError('multiple ASG\'s found for {} = {},{}'
                                 .format(tags, asg_name, asgX_name))
        except StopIteration:
            break
    return asg_name
