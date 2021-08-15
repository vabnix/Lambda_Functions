import boto3

client = boto3.client('ec2')

ebsVolumeList = client.describe_volumes()

for ebsVolume in ebsVolumeList['Volumes']:
    if ebsVolume['VolumeType'] == 'gp2':
        updateVolume = client.modify_volume(
            VolumeId=ebsVolume['VolumeId'],
            VolumeType='gp3'
        )
        print(updateVolume)
