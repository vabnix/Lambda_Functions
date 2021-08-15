from collections import defaultdict

import boto3

ec2 = boto3.client('ec2')
ec2_instance_describe = ec2.describe_instances(
    Filters=[{'Name': 'instance-state-name',
              'Values': ['running']}])
print("Original Number of Instance -", len(ec2_instance_describe['Reservations']))
# creating a list
ec2InstanceList = []


def create_cloudwatch_alarm_for_windows(NameOfInstance, InstanceId):
    print("Creating Alarm for " + NameOfInstance + "-" + InstanceId)
    cloudwatch.put_metric_alarm(
        AlarmName='CPU_Utilization_Alarm_'
                  + NameOfInstance
                  + "_[" + InstanceId + "]",
        ComparisonOperator='GreaterThanThreshold',
        EvaluationPeriods=2,
        MetricName='CPUUtilization',
        Namespace='AWS/EC2',
        Period=300,
        Statistic='Average',
        Threshold=95.0,
        ActionsEnabled=True,
        AlarmActions=[
            'arn:aws:sns:us-east-1:153617659704:DevOps_Only'
        ],
        OKActions=[
            'arn:aws:sns:us-east-1:153617659704:DevOps_Only'
        ],
        AlarmDescription='Alarm when server CPU Utilization exceeds 95%',
        Dimensions=[
            {
                'Name': 'InstanceId',
                'Value': InstanceId
            },
        ]
    )


def create_cloudwatch_alarm_for_non_windows(NameOfInstance, InstanceId):
    print("Creating Alarm for " + NameOfInstance + "-" + InstanceId)
    cloudwatch.put_metric_alarm(
        AlarmName='CPU_Utilization_Alarm_'
                  + NameOfInstance
                  + "_[" + InstanceId + "]",
        ComparisonOperator='GreaterThanThreshold',
        EvaluationPeriods=2,
        MetricName='CPUUtilization',
        Namespace='AWS/EC2',
        Period=300,
        Statistic='Average',
        Threshold=95.0,
        ActionsEnabled=True,
        AlarmActions=[
            'arn:aws:sns:us-east-1:153617659704:DevOps_Only'
        ],
        OKActions=[
            'arn:aws:sns:us-east-1:153617659704:DevOps_Only'
        ],
        AlarmDescription='Alarm when server CPU Utilization exceeds 95%',
        Dimensions=[
            {
                'Name': 'InstanceId',
                'Value': InstanceId
            },
        ]
    )


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


# What we are doing here is to identify the list of EC2 instance for which Memory Alarm needs to be created
for reservation in ec2_instance_describe['Reservations']:
    # print(len(reservation['Instances']))
    for instance in reservation['Instances']:
        if 'KeyName' in instance and instance['KeyName'] in ['lwt-prod-reporting', 'lwt-prod-mls', 'lwt-prod-rabbitmq']:
            # if 'State' in instance:
            #     for state in instance['State']:
            #         if instance['State']['Name'] == 'running':
            if 'Tags' in instance:
                for tag in instance['Tags']:
                    if tag['Key'] == "Name":
                        name = tag["Value"]
                        if name.startswith("prod-"):
                            ec2InstanceList.append(instance)

cloudwatch = boto3.client('cloudwatch')

print("Number of Instance in EC2 -", len(ec2InstanceList))

for obj in ec2InstanceList:
    InstanceName = ""
    for tag in obj['Tags']:
        if tag['Key'] == "Name":
            InstanceName = tag["Value"]
    if 'Platform' in obj and obj['Platform'] == 'windows':
        print("calling create_cloudwatch_alarm_for_windows()")
        if InstanceName != "":
            create_cloudwatch_alarm_for_windows(InstanceName, obj['InstanceId'])
    else:
        print("calling create_cloudwatch_alarm_for_non_windows()")
        if InstanceName != "":
            create_cloudwatch_alarm_for_non_windows(InstanceName, obj['InstanceId'])
    # if InstanceName != "":
    #     cloudwatch.put_metric_alarm(
    #         AlarmName='CPU_Utilization_Alarm_'
    #                   + InstanceName
    #                   + "_[" + obj['InstanceId'] + "]",
    #         ComparisonOperator='GreaterThanThreshold',
    #         EvaluationPeriods=2,
    #         MetricName='CPUUtilization',
    #         Namespace='System/Linux',
    #         Period=300,
    #         Statistic='Average',
    #         Threshold=95.0,
    #         ActionsEnabled=True,
    #         AlarmActions=[
    #             'arn:aws:sns:us-east-1:153617659704:DevOps_Only'
    #         ],
    #         OKActions=[
    #             'arn:aws:sns:us-east-1:153617659704:DevOps_Only'
    #         ],
    #         AlarmDescription='Alarm when server CPU Utilization exceeds 95%',
    #         Dimensions=[
    #             {
    #                 'Name': 'InstanceId',
    #                 'Value': obj["InstanceId"]
    #             },
    #         ]
    #     )
