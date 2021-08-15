from collections import defaultdict

import boto3

# Create IAM client
iam = boto3.client('iam')

# creating default dict
iamkeyLastUsed = defaultdict()


def delete_user_key(userName, accessKeyId):
    print(iam.delete_access_key(
        UserName=userName,
        AccessKeyId=accessKeyId
    ))


# List access keys through the pagination interface.
users = iam.list_users()
for key in users['Users']:
    paginator = iam.get_paginator('list_access_keys')
    for response in paginator.paginate(UserName=key['UserName']):
        if response['AccessKeyMetadata']:
            for tag in response['AccessKeyMetadata']:
                AccessKeyId = iam.get_access_key_last_used(
                    AccessKeyId=tag['AccessKeyId']
                )
                iamkeyLastUsed[tag['UserName']] = {
                    'UserName': tag['UserName'],
                    'AccessKeyId': tag['AccessKeyId'],
                    'Status': tag['Status'],
                    'LastUsedInfo': AccessKeyId['AccessKeyLastUsed']
                }

UserWithUnusedKey = []

for key, value in iamkeyLastUsed.items():
    UserWithUnusedKey.append(value)

for UserList in UserWithUnusedKey:
    something = UserList['LastUsedInfo']
    if something.get('LastUsedDate') is not None:
        pass
    else:
        print(UserList)
        delete_user_key(UserList['UserName'], UserList['AccessKeyId'])

