import boto3

ELB_Client = boto3.client('elbv2')

# List all autoscaling group
ELB_List = ELB_Client.describe_load_balancers()

ArnList = []

# Now that we have LB list, lets see what we got
for LB in ELB_List['LoadBalancers']:
    # print("---------------------------------------------")
    # print("LoadBalancer Name - " + LB['LoadBalancerName'])
    # print("LoadBalancer Arn - " + LB['LoadBalancerArn'])
    ArnList.append(LB['LoadBalancerArn'])
    # with LB we will find TG associated with each LB
    TG_List = ELB_Client.describe_target_groups()
    for TargetGroup in TG_List['TargetGroups']:
        for FormTg in TargetGroup['LoadBalancerArns']:
            if FormTg == LB['LoadBalancerArn']:
                # print("Target Group Name -" + TargetGroup['TargetGroupName'])
                # print("Target Group Arn -" + TargetGroup['TargetGroupArn'])
                ArnList.append(TargetGroup['TargetGroupArn'])

# To avoid duplication
ArnList = list(set(ArnList))

for Arn in ArnList:
    describeTag = ELB_Client.describe_tags(
        ResourceArns=[Arn]
    )
    for tagDescription in describeTag['TagDescriptions']:
        if len(tagDescription['Tags']) == 0:
            ELB_Client.add_tags(
                ResourceArns=[Arn],
                Tags=[
                    {
                        'Key': 'Environment',
                        'Value': 'Dev',
                    }
                ],
            )
        else:
            ExistingTags = tagDescription['Tags']
            KeyTag = [tag['Key'] for tag in ExistingTags]
            if 'Environment' not in KeyTag:
                ELB_Client.add_tags(
                    ResourceArns=[Arn],
                    Tags=[
                        {
                            'Key': 'Environment',
                            'Value': 'Dev',
                        }
                    ],
                )
