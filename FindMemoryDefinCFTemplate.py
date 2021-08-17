# We periodically run into a bug when all the memory is utilized for an ECS task, and it has trouble placing a new
# task. To resolve this we should only have 900 mb for 1 of the ECS tasks in the lowers (assuming they are on
# t3.small) In any other instance sizes, we need to ensure at least 59mb of space for the EC2 instance and ECS to
# operate successfully.

import os
import json
from collections import defaultdict

path = "path to template folder"
directories = os.listdir(path)


def get_keys(dl, keys_list):
    if isinstance(dl, dict):
        keys_list += dl.keys()
        map(lambda x: get_keys(x, keys_list), dl.values())
    elif isinstance(dl, list):
        map(lambda x: get_keys(x, keys_list), dl)


IncorrectMemoryAlloc = defaultdict()
IgnoreFileName = ["dev-chron.json", "unified-reporting-cloudformation.json"]
counter = 0

for filename in directories:
    if filename.endswith(".json") and filename.startswith("dev-"):
        if filename not in IgnoreFileName:
            counter += 1
            record = filename
            json_data = open(path + "/" + filename)
            jdata = json.load(json_data)

            resources = jdata["Resources"]["taskdefinition"]
            containers = resources["Properties"]["ContainerDefinitions"]
            Parameters = jdata["Parameters"]["InstanceType"]
            record += " Instance Type = " + Parameters["Default"]

            for container in containers:
                for key, value in container.items():
                    if key == "Memory":
                        record += " Memory = " + value
                        IncorrectMemoryAlloc[counter] = {
                            'Name': filename,
                            'InstanceType': Parameters["Default"],
                            'Memory': value
                        }

# print(IncorrectMemoryAlloc)

MemoryAlloc = list(map(list, IncorrectMemoryAlloc.items()))

for items in MemoryAlloc:
    if items[1]["InstanceType"] == "t3.micro":
        result = 959 - int(items[1]["Memory"])
        if result < 59:
            print("Revisit CF Template for: %s where Memory is %s for %s" % (
                items[1]["Name"], items[1]["Memory"], items[1]["InstanceType"]))
    if items[1]["InstanceType"] == "t3.small":
        result = 1900 - int(items[1]["Memory"])
        if result < 59:
            print("Revisit CF Template for: %s where Memory is %s for %s" % (
                items[1]["Name"], items[1]["Memory"], items[1]["InstanceType"]))


# import os
# import json
#
# path = "path to template folder"
# directories = os.listdir(path)
#
#
# def get_keys(dl, keys_list):
#     if isinstance(dl, dict):
#         keys_list += dl.keys()
#         map(lambda x: get_keys(x, keys_list), dl.values())
#     elif isinstance(dl, list):
#         map(lambda x: get_keys(x, keys_list), dl)
#
#
# IncorrectMemoryAlloc = []
# IgnoreFileName = ["dev-chron.json", "unified-reporting-cloudformation.json"]
#
# for filename in directories:
#     if filename.endswith(".json") and filename.startswith("dev-"):
#         if filename not in IgnoreFileName:
#             record = filename
#             json_data = open(path + "/" + filename)
#             jdata = json.load(json_data)
#
#             resources = jdata["Resources"]["taskdefinition"]
#             containers = resources["Properties"]["ContainerDefinitions"]
#             Parameters = jdata["Parameters"]["InstanceType"]
#             record += " Instance Type = " + Parameters["Default"]
#
#             for container in containers:
#                 for key, value in container.items():
#                     if key == "Memory":
#                         record += " Memory = " + value
#
#             print(record)
