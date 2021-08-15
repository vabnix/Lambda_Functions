import boto3

client = boto3.client('cloudformation')

response = client.list_stacks()

print(response)