import boto3

ASG_Client = boto3.client('autoscaling')

#List all autoscaling group
ASG_List = ASG_Client.describe_auto_scaling_groups()

#Lets delete new tag to each autoscaling group we have
for asg in ASG_List['AutoScalingGroups']:
    ResourceId = ""
    for tag in asg['Tags']:
        ResourceId = tag['ResourceId']
        if tag['Key'] == 'Environment':
            ASG_Client.delete_tags(
                    Tags=[
                        {
                            'ResourceId': ResourceId,
                            'ResourceType': 'auto-scaling-group',
                            'Key': 'Environment',
                            'Value': 'Dev',
                            'PropagateAtLaunch': True
                        },
                    ]
                )

