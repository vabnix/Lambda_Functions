import boto3

# Note elbv2 is for Application Load Balancers and not for Classic
ELB_Client = boto3.client('elbv2')

# List all autoscaling group
ELB_List = ELB_Client.describe_load_balancers()

ArnList = []

# Now that we have LB list, lets see what we got
for LB in ELB_List['LoadBalancers']:
    ArnList.append(LB['LoadBalancerArn'])

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
