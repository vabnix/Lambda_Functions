from datetime import datetime, timedelta
import boto3
import os

# Create CloudWatch client
cloudwatch = boto3.client('cloudwatch')

# List alarms of insufficient data through the pagination interface
responses = cloudwatch.describe_alarms(
    StateValue='INSUFFICIENT_DATA'
)

alarmToDelete = []


def cloudwatch_alarm_to_delete():
    cloudwatch.delete_alarms(
        AlarmNames=alarmToDelete
    )


# Before we delete the alarm which are not required, lets take backup of them
for response in responses['MetricAlarms']:
    time_between_last_update = datetime.now().date() - response['StateUpdatedTimestamp'].date()
    if time_between_last_update.days > 30:
        fileName = response['AlarmName'] + ".txt"
        filepath = os.path.join("./output/", fileName)
        if not os.path.exists("./output/"):
            os.makedirs("./output/")
        createFile = open(filepath, "w+")
        createFile.write(str(response))
        print(response['AlarmName'] + " not updated from -> " + str(time_between_last_update.days) + " days")
        alarmToDelete.append(response['AlarmName'])

cloudwatch_alarm_to_delete()

