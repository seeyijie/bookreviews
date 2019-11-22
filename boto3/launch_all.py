import boto3
import time
import fire

# preconditions:
# 1. there should not be any existing security groups named "50043_SECURITY_GROUP"
# 2. image id must be ubuntu 18.04
ec2 = boto3.resource('ec2')
# inputs from command line: pem key, aws ami image id of ubuntu 18.04
# launches 4 instances and returns
def launch_ec2(image, keyname): # key = 50043-keypair
    new_instances = ec2.create_instances(
    ImageId=image,
    MinCount=4, # create at least MinCount instances or dont create any
    MaxCount=4, # give me at most MaxCount instances
    InstanceType='t2.micro',
    KeyName= keyname,
    SecurityGroups=[
        '50043_SECURITY_GROUP',
    ]
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

# calls all the necessary functions to generate ip files
def write_instances(instances):
    server_types = ["react", "mongodb", "mysql", "flask"]
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
        if server_types[i] == "react":
            write_ip_to_js(instance)
        i += 1
    return None

# TODO: write a function that calls the launch_ec2 function, gets the return value and passes it to write_instances function
# function needs to take in image id and keyname
def cli(image, keyname): # default ubuntu image for 18.04 is ami-0d5d9d301c853a04a
    import setup_security_groups # runs the setup security group python file
    instances = launch_ec2(image, keyname)
    write_instances(instances)
    # at the end, call a script to scp over files to servers

if __name__ == '__main__':
  fire.Fire(cli)