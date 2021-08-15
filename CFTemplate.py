import boto3

client = boto3.client('cloudformation')

templates = client.get_template(
    StackName='dev-agent-recruiting-api'
)


def _stack_exists(stack_name):
    stacks = client.list_stacks()['StackSummaries']
    for stack in stacks:
        if stack['StackStatus'] == 'DELETE_COMPLETE':
            continue
        if stack_name == stack['StackName']:
            return True
    return False


print(templates)

# Creating CF Template Programmatically
response = client.create_stack(
    StackName='dev-vaibhav-api',
    TemplateBody='string',
    TemplateURL='string',
    Parameters=[
        {
            'ParameterKey': 'string',
            'ParameterValue': 'string',
            'UsePreviousValue': True | False,
            'ResolvedValue': 'string'
        },
    ],
    DisableRollback=False,
    RollbackConfiguration={
        'RollbackTriggers': [
            {
                'Arn': 'string',
                'Type': 'string'
            },
        ],
        'MonitoringTimeInMinutes': 123
    },
    TimeoutInMinutes=123,
    NotificationARNs=[
        'string',
    ],
    Capabilities=[
        'CAPABILITY_IAM' | 'CAPABILITY_NAMED_IAM' | 'CAPABILITY_AUTO_EXPAND',
    ],
    ResourceTypes=[
        'string',
    ],
    RoleARN='string',
    OnFailure='DO_NOTHING' | 'ROLLBACK' | 'DELETE',
    StackPolicyBody='string',
    StackPolicyURL='string',
    Tags=[
        {
            'Key': 'string',
            'Value': 'string'
        },
    ],
    ClientRequestToken='string',
    EnableTerminationProtection=True | False
)
