import boto3
import time
ec2 = boto3.resource('ec2')


new_instances = ec2.create_instances(
    # ImageId='ami-0d5d9d301c853a04a', # default ubuntu image
    ImageId='', # test using mongodb image
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