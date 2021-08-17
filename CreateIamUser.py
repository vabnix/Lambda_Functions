import boto3

client = boto3.client('iam')

ExistingUser = []


def pull_existing_user():
    users = client.list_users()
    for user in users['Users']:
        ExistingUser.append(user['UserName'])


# Now that we have users that exist in AWS Dev, lets create new users
UserToAdd = ['aazhar@vabnix.com', 'akorbiel@vabnix.com', 'apearson@vabnix.com', 'aschaffer@vabnix.com',
             'avandeworp@vabnix.com', 'blocis@vabnix.com', 'calberta@vabnix.com', 'cdickson@vabnix.com',
             'cpatrick@vabnix.com', 'cschock@vabnix.com', 'drestrepo@vabnix.com', 'ezareei@vabnix.com',
             'guppal@vabnix.com', 'hhoshyar@vabnix.com', 'hnguyen@vabnix.com', 'jsmiley@vabnix.com',
             'jstager@vabnix.com', 'kfarat@vabnix.com', 'mchugh@vabnix.com', 'mconte@vabnix.com',
             'mfullom@vabnix.com', 'mlemieux@vabnix.com', 'msimmons@vabnix.com', 'msueping@vabnix.com',
             'nkhosla@vabnix.com', 'oasenime@vabnix.com', 'rawasthi@vabnix.com', 'rbhandari@vabnix.com']


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
