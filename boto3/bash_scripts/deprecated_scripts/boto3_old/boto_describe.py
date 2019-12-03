import boto3
from botocore.exceptions import ClientError

ec2 = boto3.client('ec2')
ec2resource = boto3.resource('ec2')

response = ec2.describe_instances()
# print(response)
# print(len(response['Reservations'])) # there are 5 instances here


def list_ec2_instances():
	instances = {}
	res = ec2.describe_instances() # response object is a nested dictionary
	for r in res['Reservations']:
		for ins in r['Instances']:
			if ins['State']['Name'] == 'running':
				instances[ins['InstanceId']] = ins['PublicIpAddress']
	print(instances)

def list_images():
	res = ec2.describe_images(Owners=['self'])
	for img in res['Images']:
		print("Name: ",img['Name'])
		print("Image: ", img['ImageId'])
		print("Description: ", img['Description'])
		print("----")

def update_security_group():
    security_groups = []
    res = ec2.describe_instances()
    for r in res['Reservations']:
        for ins in r['Instances']:
            id = ins['SecurityGroups'][0]['GroupId']
            security_group = ec2resource.SecurityGroup(id)
            security_groups.append(security_group)
    return security_groups

def describe_security_groups(SECURITY_GROUP_ID):
    try:
        response = ec2.describe_security_groups(GroupIds=[SECURITY_GROUP_ID])
        print(response)
    except ClientError as e:
        print(e)

describe_security_groups(update_security_group()[0])