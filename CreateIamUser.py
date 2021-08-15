import boto3

client = boto3.client('iam')

ExistingUser = []


def pull_existing_user():
    users = client.list_users()
    for user in users['Users']:
        ExistingUser.append(user['UserName'])


# Now that we have users that exist in AWS Dev, lets create new users
UserToAdd = ['aazhar@lwolf.com', 'akorbiel@lwolf.com', 'apearson@lwolf.com', 'aschaffer@lwolf.com',
             'avandeworp@lwolf.com', 'blocis@lwolf.com', 'calberta@lwolf.com', 'cdickson@lwolf.com',
             'cpatrick@lwolf.com', 'cschock@lwolf.com', 'drestrepo@lwolf.com', 'ezareei@lwolf.com',
             'guppal@lwolf.com', 'hhoshyar@lwolf.com', 'hnguyen@lwolf.com', 'jsmiley@lwolf.com',
             'jstager@lwolf.com', 'kfarat@lwolf.com', 'mchugh@lwolf.com', 'mconte@lwolf.com',
             'mfullom@lwolf.com', 'mlemieux@lwolf.com', 'msimmons@lwolf.com', 'msueping@lwolf.com',
             'nkhosla@lwolf.com', 'oasenime@lwolf.com', 'rawasthi@lwolf.com', 'rbhandari@lwolf.com']


def update_login_profile(username):
    print("----Updating Login Profile -----")
    try:
        response = client.get_login_profile(UserName=username)
    except Exception as e:
        if e.response['ResponseMetadata']['HTTPStatusCode'] == 404:
            print('User {} has no login profile'.format(username))
            print('Creating profile...')
            create_response = client.create_login_profile(
                UserName=username,
                Password='LoneWolf!1',
                PasswordResetRequired=True
            )
            print(create_response)


def attach_user_policy(username):
    print("--- Attaching default policies ----")
    response = client.attach_user_policy(
        UserName=username,
        PolicyArn='arn:aws:iam::aws:policy/IAMUserChangePassword'
    )


def create_user_account():
    print("---- Creating User account -----")
    for username in UserToAdd:
        if username not in ExistingUser:
            response = client.create_user(
                UserName=username
            )
            update_login_profile(username)
            attach_user_policy(username)


pull_existing_user()
create_user_account()
