import boto3
import sys
import json
import argparse

VariableFileName = "./variables.json"

parser = argparse.ArgumentParser(
        description='this will look up the iam role of a running machine based on the value of the Tag Key "Name".')
parser.add_argument('-n', action='store', dest='name',
                    help="Name Tag of the machine to lookup", type=str)
args = parser.parse_args()

ServerMap = {}
client = boto3.client('ec2')

if args.name:
    # Only Print info for instances with Names (mapped to hostname -> salt top file IDs)
    # ec2 instances with no iam roles are ok since their test wont be blocked
    for Ec2Instance in client.describe_instances()['Reservations']:
        if 'Tags' in Ec2Instance['Instances'][0]:
            for TagDocument in Ec2Instance['Instances'][0]['Tags']:
                if 'Key' in TagDocument:
                    if TagDocument['Key'] == 'Name':
                        if TagDocument['Value'] == args.name:
                            if 'IamInstanceProfile' in Ec2Instance['Instances'][0]:
                                ServerMap['id'] = args.name
                                ServerMap['machine_iam_role'] = \
                                    Ec2Instance['Instances'][0]['IamInstanceProfile']['Arn'].split('/')[-1]
                                print("Found the the Name and the IAM role name, writing the following to file ..",
                                      VariableFileName)
                                print(json.dumps(ServerMap, sort_keys=True, indent=4))
                                with open(VariableFileName, 'w') as VariableFile:
                                    VariableFile.write(json.dumps(ServerMap, sort_keys=True, indent=4))
                                sys.exit(0)
    print("Couldn't find the the Name and/or the IAM role name")
    sys.exit(2)


else:
    print("provide -h for help ")
    sys.exit(2)
