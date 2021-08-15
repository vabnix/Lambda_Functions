import boto3

ec2 = boto3.client("ec2")
reservations = ec2.describe_instances(
    Filters=[{'Name': 'instance-state-name',
              'Values': ['running']}])["Reservations"]

list = []


def element_count(data):
    count = {}
    for element in data:
        count[element] = count.get(element, 0) + 1
    return count


for reservation in reservations:
    for instance in reservation['Instances']:
        list.append(instance['InstanceType'])

counter = element_count(list)

print(counter)
