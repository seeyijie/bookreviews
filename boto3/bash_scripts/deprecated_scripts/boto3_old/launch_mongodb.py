# not in use
import boto3
import time
ec2 = boto3.resource('ec2')


new_instances = ec2.create_instances(
    ImageId='ami-0d5d9d301c853a04a', # replace this with finalized monogodb image
    MinCount=1, # create at least MinCount instances or dont create any
    MaxCount=1, # give me at most MaxCount instances
    InstanceType='t2.micro',
    KeyName='50043-keypair',
    SecurityGroups=[
        '50043_SECURITY_GROUP_TEST',
    ]
)

for instance in new_instances:
    instance.wait_until_running()
    instance.reload() # update attributes
    print(f"new instance: {instance}")
    print(instance.public_ip_address)
    print(instance.key_name)
    print(instance.launch_time)
    print("\n")
    # write into bash files
    with open (f"../scripts/server_scripts/config/config_mongodb.sh", 'w') as f:
        f.write(f'#!/bin/bash\nserver_ip="{instance.public_ip_address}"\npublic_key="{instance.key_name}.pem"\nusername="ubuntu"')

    # write IP addresses to a text file (scp this to the new server)
    f = open(f"../scripts/server_scripts/config/config_mongodb_ip.txt", "w")
    f.write(f"{instance.public_ip_address}")
    f.close()
    
    # launch scripts to run commands to launch database services
