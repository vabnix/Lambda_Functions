import boto3

ec2 = boto3.client("ec2")
reservations = ec2.describe_instances(
    Filters=[{'Name': 'instance-state-name',
              'Values': ['running']}])

InstanceTypeList = []


def element_count(data):
    count = {}
    for element in data:
        count[element] = count.get(element, 0) + 1
    return count


for reservation in reservations['Reservations']:
    for instance in reservation['Instances']:
        InstanceTypeList.append(instance['InstanceType'])

counter = element_count(InstanceTypeList)

print(counter)
