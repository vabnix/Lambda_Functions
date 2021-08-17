import boto3

client = boto3.client('rds')
response = client.describe_db_clusters()


response = client.create_db_cluster(
    AvailabilityZones=['us-east-2a', 'us-east-2b', 'us-east-2c'],
    BackupRetentionPeriod=7,
    CharacterSetName='string',
    DatabaseName='AWS-RDS-DB-01',
    DBClusterIdentifier='dev-LW-cluster',
    DBClusterParameterGroupName='solarwinds',
    VpcSecurityGroupIds=[{'VpcSecurityGroupId': 'sg-903ab7e6', 'Status': 'active'}],
    DBSubnetGroupName='default-vpc-6d69c704',
    Engine='aurora-postgresql',
    EngineVersion='12.5-R1',
    Port=5432,
    MasterUsername='vabnix',
    MasterUserPassword='string',
    OptionGroupName='string',
    PreferredBackupWindow='10:26-10:56',
    PreferredMaintenanceWindow='sun:05:00-sun:05:30',
    ReplicationSourceIdentifier='string',
    Tags=[
        {
            'Key': 'string',
            'Value': 'string'
        },
    ],
    StorageEncrypted=True,
    KmsKeyId='arn:aws:kms:us-east-1:058367129984:key/8fb43078-b592-4723-b398-11082224e943',
    EnableIAMDatabaseAuthentication=False,
    BacktrackWindow=123,
    EnableCloudwatchLogsExports=[
        'string',
    ],
    EngineMode='provisioned',
    ScalingConfiguration={
        'MinCapacity': 123,
        'MaxCapacity': 123,
        'AutoPause': True|False,
        'SecondsUntilAutoPause': 123,
        'TimeoutAction': 'string'
    },
    DeletionProtection=False,
    GlobalClusterIdentifier='string',
    EnableHttpEndpoint=False,
    CopyTagsToSnapshot=False,
    Domain='string',
    DomainIAMRoleName='string',
    EnableGlobalWriteForwarding=True|False,
    SourceRegion='string'
)