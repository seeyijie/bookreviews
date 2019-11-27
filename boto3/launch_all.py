import time
import fire
import subprocess
import boto3
from botocore.exceptions import ClientError

# preconditions:
# 1. there should not be any existing security groups named "50043_SECURITY_GROUP"
# 2. image id must be ubuntu 18.04
ec2 = boto3.resource('ec2')
# inputs from command line: pem key, aws ami image id of ubuntu 18.04
# launches 4 instances and returns
def launch_ec2(image, keyname, count, userdata): # key = 50043-keypair
    new_instances = ec2.create_instances(
    ImageId=image,
    MinCount=count, # create at least MinCount instances or dont create any
    MaxCount=count, # give me at most MaxCount instances
    InstanceType='t2.micro',
    KeyName= keyname,
    SecurityGroups=[
        '50043_SECURITY_GROUP',
    ],
    UserData=userdata
    )
    return new_instances

# write the IP address for one instance into a text file
def write_ip_addresses(instance, instance_type):
    with open(f"ip_addresses/config_{instance_type}_ip.txt", "w") as f:
        f.write(f"{instance.public_ip_address}")
    return None

# write the IP address for flask server into one js file
def write_ip_to_js(instance):
    with open(f"config_files/config.js", "w") as f:
        f.write(f'export const flaskip = "http://{instance.public_ip_address}:5000"')
    return None

# writes instance information (mongodb, flask, react, mysql)
def write_config_files(instance, instance_type):
    # write into bash files
    with open (f"config_files/config_{instance_type}.sh", 'w') as f:
        f.write(f'#!/bin/bash\nserver_ip="{instance.public_ip_address}"\npublic_key="{instance.key_name}.pem"\nusername="ubuntu"')
    return None

def write_fingerprint_config(instance, instance_type):
    with open(f"config_files/fingerprint_{instance_type}.sh", 'w') as f:
        f.write(f'#!/bin/bash\nssh-keygen -R {instance.public_ip_address}\nssh-keyscan -t ecdsa -H {instance.public_ip_address} >> ~/.ssh/known_hosts')

# calls all the necessary functions to generate ip files
def write_instances(instances, server_types):
    i = 0
    for instance in instances:
        instance.wait_until_running()
        instance.reload() # update attributes
        print(f"\n******** {server_types[i]} server info ********")
        print(f"new instance: {instance.instance_id}")
        print(instance.public_ip_address)
        print(instance.key_name)
        print(instance.launch_time)

        # write IP addresses and config files for respective images
        write_config_files(instance, server_types[i])
        write_ip_addresses(instance, server_types[i])
        # write_fingerprint_config(instance, server_types[i])
        if server_types[i] == "react":
            write_ip_to_js(instance)
        i += 1
    return None

def create_security_group(group_name, description):
    ec2_client = boto3.client('ec2')
    response = ec2_client.describe_vpcs()
    vpc_id = response.get('Vpcs', [{}])[0].get('VpcId', '')

    try:
        response = ec2_client.create_security_group(GroupName=group_name,
                                            Description=description,
                                            VpcId=vpc_id)
        security_group_id = response['GroupId']
        print('Security Group Created %s in vpc %s.' % (security_group_id, vpc_id))

        data = ec2_client.authorize_security_group_ingress(
            GroupId=security_group_id,
            IpPermissions=[
                {'IpProtocol': 'tcp',
                'FromPort': 80,
                'ToPort': 80,
                'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
                {'IpProtocol': 'tcp',
                'FromPort': 22,
                'ToPort': 22,
                'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
                # for mysql
                {'IpProtocol': 'tcp',
                'FromPort': 3306,
                'ToPort': 3306,
                'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
                # for mongodb
                {'IpProtocol': 'tcp',
                'FromPort': 27017,
                'ToPort': 27017,
                'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
                # for flask
                {'IpProtocol': 'tcp',
                'FromPort': 5000,
                'ToPort': 5000,
                'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
                # for react
                {'IpProtocol': 'tcp',
                'FromPort': 3000,
                'ToPort': 3000,
                'IpRanges': [{'CidrIp': '0.0.0.0/0'}]}
            ])
        print('Ingress Successfully Set %s' % data)
    except ClientError as e:
        print(e)
    return None
    
# function needs to take in image id and keyname
def cli(image, keyname): # default ubuntu image for 18.04 is ami-0d5d9d301c853a04a
    # create security group
    create_security_group("50043_SECURITY_GROUP", "security group for 50043 database project")

    # server_types = ["react", "mongodb", "mysql", "flask"]
    server_types = ["mysql"] # for testing purposes


    f1 = open("bash_scripts/user_data/ud_mysql.sh","r")
    mysql_ud = f1.read()

    user_data = {"mysql": mysql_ud}

    # launch instances
    instances = []
    for i in range(len(server_types)):
        # TODO: add inputs for size of EC2, eg t2.micro
        instance = launch_ec2(image, keyname, 1, user_data[server_types[i]])
        instances.append(instance)
            
        # write ip addresses into text files and bash files
        write_instances(instance, [server_types[i]])

    

    # for server in server_types:
    #     subprocess.call([f'./bash_scripts/master_scripts/deploy_{server}.sh'])

    # TODO: at the end, call a script to scp over files to servers

if __name__ == '__main__':
  fire.Fire(cli)