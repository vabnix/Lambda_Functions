import json

import requests

authorization = "Bearer 00D7b0000004cZl!AR8AQKCgmwFtlihHiddJasszrMXBZ9uFp" \
                "..62ridrzkFITRCwSVmXjFhdsMTzlqxmzEKMs_4Ru0Abc49bw1r9EY0LCBYrsIh "
baseUrl = "https://lonewolf--lwfull.my.salesforce.com"
headers = {'content-type': 'application/json', 'Authorization': authorization}


def get_hosting_information(accountId):
    # accountUrl = "/services/data/v52.0/sobjects/Account/{accountId}"
    formedAccountUrl = baseUrl + accountId
    AccountResponse = requests.get(formedAccountUrl, headers=headers)
    dump = json.loads(AccountResponse.content)
    hosting_server = dump['brokerWOLF_Hosting_Server__c']
    print(dump['Penderis_Code__c'] + " => " + dump['Name'] + " => " + str(
        hosting_server))


formedUrl = baseUrl + "/services/data/v52.0/query/?q=SELECT+name+from+Account"
response = requests.get(formedUrl, headers=headers)
accountDump = json.loads(response.content)
for account in accountDump['records']:
    get_hosting_information(account['attributes']['url'])
print(accountDump)
