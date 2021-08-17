#!/usr/bin/env python3

from pathlib import Path

path = ['local directory path']

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

