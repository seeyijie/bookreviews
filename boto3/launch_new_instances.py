import boto3
import time
ec2 = boto3.resource('ec2')

# create a new EC2 instance. Running this part of the script automatically creates a new ec2 instance
# documentation for waiters: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#waiters

# new_instance is a list of ec2 objects. Can run methods on ec2 objects
new_instances = ec2.create_instances(
    # ImageId='ami-0d5d9d301c853a04a', # default ubuntu image
    ImageId='ami-01fd5140d19a25af9', # test using mongodb image
    MinCount=1, # create at least MinCount instances or dont create any
    MaxCount=1, # give me at most MaxCount instances
    InstanceType='t2.micro',
    KeyName='50043-keypair',
    SecurityGroups=[
        '50043_SECURITY_GROUP_TEST',
    ]
)

# filenames = ["config_flask", "config_mongodb", "config_mysql"] # use this for generating all
filenames = ["config_mongodb"]
index = 0
# wait for this instance to be running then exit
for instance in new_instances:
    # instance is an ec2.Instance() object
    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#instance
    instance.wait_until_running()
    instance.reload() # update attributes
    print(f"new instance: {instance}")
    print(instance.public_ip_address)
    print(instance.key_name)
    print(instance.launch_time)
    print("\n")

    # write configuration information into configuration bash file
    with open (f"../scripts/server_scripts/config/{filenames[index]}.sh", 'w') as f:
        f.write(f'#!/bin/bash\nserver_ip="{instance.public_ip_address}\n"public_key="{instance.key_name}.pem"\nusername="ubuntu"')

    # write IP addresses to a text file (scp this to the new server)
    f = open(f"../scripts/server_scripts/config/{filenames[index]}_ip.txt", "w")
    f.write(f"{instance.public_ip_address}")
    f.close()

    index += 1



