import boto3


def apply_tag_on_ec2():
    print("Applying Tags on EC2......")
    ec2 = boto3.client("ec2")
    reservations = ec2.describe_instances(
        Filters=[{'Name': 'instance-state-name',
                  'Values': ['running']}])["Reservations"]
    mytags = [
        {
            "Key": "BillingUnit",
            "Value": "LionDesk"
        }]
    for reservation in reservations:
        for each_instance in reservation["Instances"]:
            ec2.create_tags(
                Resources=[each_instance["InstanceId"]],
                Tags=mytags
            )


def apply_tag_on_load_balancers():
    print("Applying Tags on LoadBalancers......")
    ELB_Client = boto3.client('elbv2')
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
                            'Key': 'BillingUnit',
                            'Value': 'LionDesk',
                        }
                    ],
                )
            else:
                ExistingTags = tagDescription['Tags']
                KeyTag = [tag['Key'] for tag in ExistingTags]
                if 'BillingUnit' not in KeyTag:
                    ELB_Client.add_tags(
                        ResourceArns=[Arn],
                        Tags=[
                            {
                                'Key': 'BillingUnit',
                                'Value': 'LionDesk',
                            }
                        ],
                    )


def apply_tag_on_target_group():
    print("Applying Tags on Target Group......")
    ELB_Client = boto3.client('elbv2')
    ELB_List = ELB_Client.describe_load_balancers()
    ArnList = []
    for LB in ELB_List['LoadBalancers']:
        # with LB we will find TG associated with each LB
        TG_List = ELB_Client.describe_target_groups()
        for TargetGroup in TG_List['TargetGroups']:
            for FormTg in TargetGroup['LoadBalancerArns']:
                if FormTg == LB['LoadBalancerArn']:
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
                            'Key': 'BillingUnit',
                            'Value': 'LionDesk',
                        }
                    ],
                )
            else:
                ExistingTags = tagDescription['Tags']
                KeyTag = [tag['Key'] for tag in ExistingTags]
                if 'BillingUnit' not in KeyTag:
                    ELB_Client.add_tags(
                        ResourceArns=[Arn],
                        Tags=[
                            {
                                'Key': 'BillingUnit',
                                'Value': 'LionDesk',
                            }
                        ],
                    )


def apply_tag_on_auto_scaling_groups():
    print("Applying Tags on ASG......")
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
            if 'BillingUnit' not in KeyTag:
                ASG_Client.create_or_update_tags(
                    Tags=[
                        {
                            'ResourceId': ResourceId,
                            'ResourceType': 'auto-scaling-group',
                            'Key': 'BillingUnit',
                            'Value': 'LionDesk',
                            'PropagateAtLaunch': True
                        }
                    ]
                )


def apply_tag_on_s3_buckets():
    client = boto3.client('s3')
    bucketList = client.list_buckets()
    for Bucket in bucketList['Buckets']:
        s3 = boto3.resource('s3')
        try:
            response = client.get_bucket_tagging(Bucket=Bucket['Name'])
            if not response['TagSet']:
                client.put_bucket_tagging(
                    Bucket=Bucket['Name'],
                    Tagging={
                        'TagSet': [
                            {
                                'Key': 'BillingUnit',
                                'Value': 'LionDesk'
                            },
                        ]
                    }
                )
            else:
                bucket_tagging = s3.BucketTagging(Bucket['Name'])
                tags = bucket_tagging.tag_set
                print("Updating Bucket - " + Bucket['Name'])
                tags.append({'Key': 'BillingUnit', 'Value': "LionDesk"})
                Set_Tag = bucket_tagging.put(Tagging={'TagSet': tags})
                print("--UPDATED--")
        except Exception as e:
            pass


apply_tag_on_ec2()
apply_tag_on_load_balancers()
apply_tag_on_target_group()
apply_tag_on_auto_scaling_groups()
# apply_tag_on_s3_buckets()
