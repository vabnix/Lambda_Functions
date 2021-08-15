#!/usr/bin/env python3

from pathlib import Path

path = ['/Users/vaibhavsrivastava/Documents/LWOLF/AWS_SSM/dev/RunResults/dev-lockbit-scan/5d4eb427-571e-4304-bc2c-79ce46f16b11',
        '/Users/vaibhavsrivastava/Documents/LWOLF/AWS_SSM/stg/RunResults/stg-lockbit-scan/e645964c-a42c-4bc3-8390-7dc1c6347d5d',
       '/Users/vaibhavsrivastava/Documents/LWOLF/AWS_SSM/pre/RunResults/pre-lockbit-scan/63435af9-ef51-4083-b7bf-9f6435b36813',
        '/Users/vaibhavsrivastava/Documents/LWOLF/AWS_SSM/prod/RunResults/prod-lockbit-scan/55bdf832-d5ba-4254-9728-c6038b3b36aa']

for envPath in path:
    Instance = 0
    Found = 0
    InstanceList = []
    if 'dev' in envPath:
        print("----------------------------")
        print("--- Scanning Dev Results ---")
        print("----------------------------")
    elif 'stg' in envPath:
        print("----------------------------")
        print("--- Scanning Stg Results ---")
        print("----------------------------")
    elif 'pre' in envPath:
        print("----------------------------")
        print("--- Scanning Pre Results ---")
        print("----------------------------")
    elif 'prod' in envPath:
        print("----------------------------")
        print("--- Scanning Prod Results ---")
        print("----------------------------")

    for path in Path(envPath).iterdir():
        InstanceList.append(path.name)
        Instance += 1
        fixedPath = "/awsrunShellScript/0.awsrunShellScript/stdout"
        new_file_path = str(path) + str(fixedPath)
        if Path(new_file_path).exists():
            stringToFind = 'lockbit'
            try:
                file1 = open(new_file_path, "r")
                readfile = file1.read()
                if stringToFind in readfile:
                    print('Keyword -', stringToFind, ' Found In File', new_file_path)
                    Found += 1
                    print(readfile)
                else:
                    pass

                # closing a file
                file1.close()
            except Exception as e:
                print('File cannot be opened', e)

    print("No. of Instance Scanned =", Instance)
    print("Lockbit file found in no. of Instance = ", Found)
    print("Instance Scanned :")
    print(InstanceList)

