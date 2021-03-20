import boto3

ec2 = boto3.client("ec2")
reservations = ec2.describe_instances(
    Filters=[{'Name': 'instance-state-name',
              'Values': ['running']}])["Reservations"]
mytags = [
    {
        "Key": "Environment",
        "Value": "Dev"
    }]
for reservation in reservations:
    for each_instance in reservation["Instances"]:
        ec2.create_tags(
            Resources=[each_instance["InstanceId"]],
            Tags=mytags
        )
