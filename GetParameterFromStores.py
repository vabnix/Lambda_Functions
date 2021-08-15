import boto3

client = boto3.client('ssm')

parameters = client.describe_parameters()['Parameters']

print(parameters)
