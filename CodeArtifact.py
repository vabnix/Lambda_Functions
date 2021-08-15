import boto3

client = boto3.client('codeartifact')


def get_domain_list():
    response = client.list_domains()
    print(response)


def get_repository_list():
    response = client.list_repositories()
    print(response)


def get_npm_package_list():
    response = client.list_packages(
        domain='lonewolf-technologies',
        repository='node-repository',
        format='npm'
    )
    return response


def delete_packages_from_npm():
    packagelist = get_npm_package_list()
    for package in packagelist['packages']:
        packageWithVersion = client.list_package_versions(
            domain='lonewolf-technologies',
            repository='node-repository',
            format='npm',
            package=package['package']
        )
        print(packageWithVersion)
        response = client.delete_package_versions(
            domain='lonewolf-technologies',
            repository='node-repository',
            format='npm',
            package=packageWithVersion['package'],
            versions=[
                packageWithVersion['defaultDisplayVersion'],
            ]
        )
        print(response)


delete_packages_from_npm()
