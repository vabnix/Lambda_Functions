import boto3

ASG_Client = boto3.client('autoscaling')

# List all autoscaling group
ASG_List = ASG_Client.describe_auto_scaling_groups()

# Lets add new tag to each autoscaling group we have
for asg in ASG_List['AutoScalingGroups']:
    ResourceId = ""
    if len(asg['Tags']) != 0:
        ExistingTags = asg['Tags']
        for tag in asg['Tags']:
            ResourceId = tag['ResourceId']
        KeyTag = [tag['Key'] for tag in ExistingTags]
        if 'Environment' not in KeyTag:
            ASG_Client.create_or_update_tags(
                Tags=[
                    {
                        'ResourceId': ResourceId,
                        'ResourceType': 'auto-scaling-group',
                        'Key': 'BillingUnit',
                        'Value': 'vabnix',
                        'PropagateAtLaunch': True
                    }
                ]
            )
