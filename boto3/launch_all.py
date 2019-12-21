import os

import fire
from botocore.exceptions import ClientError

import boto3

ec2 = boto3.resource('ec2')
def launch_ec2(image, keyname, count, userdata, instancetype): # key = 50043-keypair , no .pem
    new_instances = ec2.create_instances(
    ImageId=image,
    MinCount=count, # create at least MinCount instances or dont create any
    MaxCount=count, # give me at most MaxCount instances
    InstanceType=instancetype,
    KeyName= keyname,
    SecurityGroups=[
        '50043_SECURITY_GROUP',
    ],
    UserData=userdata
    )
    return new_instances

# write the IP address for one instance into a text file
def write_ip_addresses(instance, instance_type, folder="ip_addresses"):
    if not os.path.isdir(folder):
        os.mkdir(folder)
    fname = "config_{}_ip.txt".format(instance_type)
    with open(os.path.join(folder, fname), 'w') as f:
        f.write(str(instance.public_ip_address))

# write the IP address for flask server into one js file
def write_ip_to_js(instance, folder="config_files"):
    if not os.path.isdir(folder):
        os.mkdir(folder)
    fname = "config.js"
    content = 'export const flaskip = "http://{}:5000"'.format(instance.public_ip_address)
    with open(os.path.join(folder, fname), 'w') as f:
        f.write(str(content))

# writes instance information (mongodb, flask, react, mysql) into bash files
def write_config_files(instance, instance_type, folder="config_files"):
    if not os.path.isdir(folder):
        os.mkdir(folder)
    fname = "config_{}.sh".format(instance_type)
    content = "\n".join([
        "#!/bin/bash",
        'server_ip = "{}"'.format(instance.public_ip_address),
        'public_key = "{}.pem"'.format(instance.key_name),
        'username="ubuntu"',
    ])
    with open(os.path.join(folder, fname), 'w') as f:
        f.write(str(content))

def write_metadata(instance, instance_type, folder="metadata"):
    if not os.path.isdir(folder):
        os.mkdir(folder)
    fname = "meta_data_{}.txt".format(instance_type)
    with open(os.path.join(folder, fname), 'w') as f:
        f.write(str(instance.instance_id))

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
        write_metadata(instance, server_types[i])
        if server_types[i] == "flask":
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

# def edit_script(filename, ipList):
#     with open(filename, "r") as file:
#         lines = file.readlines()
#     for ip in range(len(ipList)):
#         lines[ip+1] = "ip_{ip}={ipList[ip]}" + "\n"
#     with open(filename, "w") as file:
#         for line in lines:
#             file.write(line)
    
# function needs to take in image id and keyname
# "Main function"
def cli(image, keyname, instancetype='t2.micro'): # default ubuntu image for 18.04 is ami-0d5d9d301c853a04a
    # create security group
    create_security_group("50043_SECURITY_GROUP", "security group for 50043 database project")

    # storing user data files into strings
    f1 = open("bash_scripts/user_data/ud_mysql.sh","r")
    mysql_ud = f1.read()
    f2 = open("bash_scripts/user_data/ud_mongodb.sh","r")
    mongodb_ud = f2.read()
    f3 = open("bash_scripts/user_data/ud_flask.sh","r")
    flask_ud = f3.read()
    f4 = open("bash_scripts/user_data/ud_react.sh","r")
    react_ud = f4.read()

    # user data storing paths to user data scripts
    user_data = {"mysql": mysql_ud, "mongodb" : mongodb_ud, "flask" : flask_ud, "react" : react_ud}

    # launch instances
    server_types = ["mongodb", "mysql", "flask", "react"]
    for i in range(len(server_types)):
        # launch the actual instance
        instance = launch_ec2(image, keyname, 1, user_data[server_types[i]], instancetype)
        # write ip addresses into text files and bash files
        write_instances(instance, [server_types[i]])

if __name__ == '__main__':
  fire.Fire(cli)