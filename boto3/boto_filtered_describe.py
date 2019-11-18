import boto3
from botocore.exceptions import ClientError

ec2 = boto3.client('ec2')

class ec2_instance():

    def __init__(self, instance_id, public_ip, keyname, launch_time):
        self.instance_id = instance_id
        self.public_ip = public_ip
        self.keyname = keyname
        self.launch_time = launch_time
    
    def get_id(self):
        return self.instance_id
    
    def get_public_ip(self):
        return self.public_ip

    def get_keyname(self):
        return self.keyname

    def get_launch_time(self):
        return self.launch_time

# lists all running instances
def list_ec2_instances_info():
    instances = {}
    res = ec2.describe_instances(
        Filters = [{'Name': 'instance-state-name', 'Values': ['running']}]
    )
    index = 0
    for reservation in res['Reservations']:
        for instance in reservation['Instances']:
            # instance object
            ec2_inst = ec2_instance(
                instance['InstanceId'],
                instance['PublicIpAddress'],
                instance['KeyName'],
                instance['LaunchTime'],
            )
            
            instances[index] = ec2_inst # create a dictionary storing instance objects
            index += 1
    return instances

running_instances = list_ec2_instances_info()
for i in running_instances.keys():
    print(f"Instance ID: {running_instances[i].get_id()}\nInstance IP: {running_instances[i].get_public_ip()}\nInstance Key: {running_instances[i].get_keyname()}\nInstance LaunchTime: {running_instances[i].get_launch_time()}\n")