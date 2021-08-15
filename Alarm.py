from collections import defaultdict

import boto3

# Connect to EC2
ec2 = boto3.resource('ec2')

# Get information for all running instances
running_instances = ec2.instances.filter(Filters=[{
    'Name': 'instance-state-name',
    'Values': ['running']}])

ec2info = defaultdict()
for instance in running_instances:
    for tag in instance.tags:
        if 'Name'in tag['Key']:
            name = tag['Value']
    # Add instance info to a dictionary
    ec2info[instance.id] = {
        'Name': name,
        'id': instance.id,
        'counter': 0
    }

list = []
setList = []

updateinfo = defaultdict()

attributes = ['Name', 'id']
for instance_id, instance in ec2info.items():
    for key in attributes:
        if key == 'Name':
            list.append(instance[key])
            counter = instance['counter']
            if instance[key] not in setList:
                instance['counter'] = counter + 1
            if instance[key] in setList:
                #now at this point i should have a way to find out the counter for name that exist in system
                instance['counter'] = counter + 2
            setList = set(list)
        print("{0}: {1} : {2}".format(key, instance[key], instance))
    print("------")

# attributes = ['Name', 'id']
# for instance_id, instance in ec2info.items():
#     for key in attributes:
#         if key == 'Name':
#             list.append(instance[key])
#         print("{0}: {1}".format(key, instance[key]))
#         setList = set(list)
#     print("------")