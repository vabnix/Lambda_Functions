import boto3

ec2 = boto3.client("ec2")
reservations = ec2.describe_instances(
    Filters=[{'Name': 'instance-state-name',
              'Values': ['running']}])["Reservations"]
mytags = [
    {
        "Key": "Environment",
        "Value": "Prod"
    }]
for reservation in reservations:
    for each_instance in reservation["Instances"]:
        if each_instance['KeyName'] == 'vabnix-prod-rabbitmq' or each_instance['KeyName'] == 'vabnix-prod-mls':
            ec2.create_tags(
                Resources=[each_instance["InstanceId"]],
                Tags=[
                    {
                        "Key": "Environment",
                        "Value": "Prod"
                    }
                ]
            )
        elif each_instance['KeyName'] == ' vabnix-prod-reporting':
            ec2.create_tags(
                Resources=[each_instance["InstanceId"]],
                Tags=[
                    {
                        "Key": "Environment",
                        "Value": "Prod"
                    }
                ]
            )
        else:
            pass
