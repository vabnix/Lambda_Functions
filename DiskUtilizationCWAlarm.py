from collections import defaultdict

import boto3

ec2 = boto3.client('ec2')
ec2_instance_describe = ec2.describe_instances()

# creating a list
list = []


def get_environment_name(vpcId):
    if vpcId == 'vpc-67110801':
        return 'DEV'
    elif vpcId == 'vpc-5cf54025':
        return 'STG'
    elif vpcId == 'vpc-aea911d6':
        return 'PRE'
    elif vpcId == 'vpc-0ee65477':
        return 'PROD'
    else:
        return 'UNKNOWN'


TagNameList = []
InstanceWithOneInstance = []
InstanceWithTwoInstance = []
InstanceWithThreeInstance = []


def element_count(data):
    count = {}
    for element in data:
        count[element] = count.get(element, 0) + 1
    return count


# What we are doing here is to identify the list of EC2 instance for which Memory Alarm needs to be created
for res in ec2_instance_describe['Reservations']:
    for instance in res['Instances']:
        if len(instance['Tags']) != 0:
            for tag in instance['Tags']:
                if tag['Key'] == "Name":
                    if tag['Value'] not in ['prod-url-to-pdf-server-cluster-member',
                                            'production-rabbitmq-autocluster-member',
                                            'prod-transform-service-cluster-member',
                                            'prod-bw-data-storage-service']:
                        TagNameList.append(tag['Value'])
                        list.append(instance)

counter = element_count(TagNameList)

for elements in list:
    if len(elements['Tags']) != 0:
        for tag in elements['Tags']:
            if tag['Key'] == "Name":
                if counter[tag['Value']] == 1:
                    InstanceWithOneInstance.append(elements)
                elif counter[tag['Value']] == 2:
                    InstanceWithTwoInstance.append(elements)
                elif counter[tag['Value']] == 3:
                    InstanceWithThreeInstance.append(elements)



ec2info = defaultdict()
for instance in InstanceWithTwoInstance:
    for tag in instance['Tags']:
        if tag['Key'] == "Name":
            name = tag['Value']
    # Add instance info to a dictionary
    ec2info[instance['InstanceId']] = {
        'Name': name,
        'id': instance['InstanceId'],
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
                # now at this point i should have a way to find out the counter for name that exist in system
                instance['counter'] = counter + 2
            setList = set(list)

newList = []

for key, value in ec2info.items():
    newList.append(value)

cloudwatch = boto3.client('cloudwatch')

for obj in newList:
    InstanceName = obj["Name"]
    print(InstanceName)
    counter = str(obj["counter"])
    if InstanceName != "":
        cloudwatch.put_metric_alarm(
            AlarmName='Disk_Utilization_Alarm_'
                      + InstanceName
                      + "_"+counter,
            ComparisonOperator='GreaterThanThreshold',
            EvaluationPeriods=2,
            MetricName='LogicalDisk % Free Space',
            Namespace='CWAgent',
            Period=300,
            Statistic='Average',
            Threshold=10,
            ActionsEnabled=True,
            AlarmActions=[
                'arn:aws:sns:us-east-1:153617659704:DevOps_Only'
            ],
            OKActions=[
                'arn:aws:sns:us-east-1:153617659704:DevOps_Only'
            ],
            AlarmDescription='Alarm when server Disk Utilization exceeds 90%',
            Dimensions=[
                {
                    'Name': 'InstanceId',
                    'Value': obj["id"]
                },
            ]
        )
