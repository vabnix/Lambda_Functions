import boto3

ec2 = boto3.client('ec2')
ec2_instance_describe = ec2.describe_instances()

# creating a list
list = []


def get_environment_name(vpcId):
    if vpcId == 'vpc-xxxxxxx':
        return 'DEV'
    elif vpcId == 'vpc-xxxx5':
        return 'STG'
    elif vpcId == 'vpc-xxxxxx6':
        return 'PRE'
    elif vpcId == 'vpc-xxxxxxxx1':
        return 'PROD'
    else:
        return 'UNKNOWN'


UpdatedList = []


def update_list_with_counter():
    for instanceFromList in list:
        instanceFromList.update({'counter': "1"})
        UpdatedList.append(instanceFromList)


for res in ec2_instance_describe['Reservations']:
    for instance in res['Instances']:
        list.append(instance)
    update_list_with_counter()

# Now lets create cloudwatch client
cloudwatch = boto3.client('cloudwatch')

# Creating cloudwatch event alarm for each instance id
#
for obj in UpdatedList:
    InstanceName = ""
    if len(obj['Tags']) != 0:
        for tag in obj['Tags']:
            if tag['Key'] == "Name":
                InstanceName = tag['Value']
    if InstanceName != "":
        cloudwatch.put_metric_alarm(
            AlarmName='Memory_Utilization_for_'
                      + get_environment_name(obj['VpcId'])
                      + "_Env_" + InstanceName
                      + "_"
                      + obj['counter'],
            ComparisonOperator='GreaterThanThreshold',
            EvaluationPeriods=2,
            MetricName='MemoryUtilization',
            Namespace='System/Linux',
            Period=300,
            Statistic='Average',
            Threshold=90.0,
            ActionsEnabled=True,
            AlarmActions=[
                'arn:aws:sns:us-east-1:xxxxxxxxxx:DevOps_Only'
            ],
            OKActions=[
                'arn:aws:sns:us-east-1:xxxxxxxxxx:DevOps_Only'
            ],
            AlarmDescription='Alarm when server Memory exceeds 90%',
            Dimensions=[
                {
                    'Name': 'InstanceId',
                    'Value': obj['InstanceId']
                },
            ]
        )
