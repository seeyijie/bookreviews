# not in use
import boto3
import time
import fire

ec2 = boto3.resource('ec2')

def launch_ec2(image):
    new_instances = ec2.create_instances(
    ImageId=image,
    MinCount=1, # create at least MinCount instances or dont create any
    MaxCount=1, # give me at most MaxCount instances
    InstanceType='t2.micro',
    KeyName='50043-keypair',
    SecurityGroups=[
        '50043_SECURITY_GROUP',
    ]
    )
    return new_instances

def describe_instances(instances, instance_type, write_js):
    for instance in instances:
        instance.wait_until_running()
        instance.reload() # update attributes
        print(f"new instance: {instance}")
        print(instance.public_ip_address)
        print(instance.key_name)
        print(instance.launch_time)
        print("\n")
        # write into bash files
        with open (f"../scripts/server_scripts/config/config_{instance_type}.sh", 'w') as f:
            f.write(f'#!/bin/bash\nserver_ip="{instance.public_ip_address}"\npublic_key="{instance.key_name}.pem"\nusername="ubuntu"')

        # write IP addresses to a text file (scp this to the new server)
        with open(f"../scripts/server_scripts/config/config_{instance_type}_ip.txt", "w") as f:
            f.write(f"{instance.public_ip_address}")

        if write_js == 1:
            create_js_ip(instance.public_ip_address)

def create_js_ip(ip_address):
    with open(f"../react-end/src/Data/config.js", "w") as f:
        f.write(f'export const flaskip = "http://{ip_address}:5000"')

def cli(mongodb="n", mysql="n", flask="n"):
    # replace images here with actual finalized images
    images = {"mongo_image":"ami-01fd5140d19a25af9", "mysql_image":"ami-0d5d9d301c853a04a","flask_image":"ami-0d5d9d301c853a04a"}
    
    # mongodb
    if mongodb.lower() == "y":
        print("launching mongodb instance...")
        instance = launch_ec2(images["mongo_image"])
        describe_instances(instance, "mongodb", 0)
    elif mongodb.lower() == "n":
        print("no mongodb selected")
    else:
        print("Invalid option. Use 'y' to deploy or ignore parameter")

    # mysql
    if mysql.lower() == "y":
        print("launching mysql instance...")
        instance = launch_ec2(images["mysql_image"])
        describe_instances(instance, "mysql", 0)
    elif mysql.lower() == "n":
        print("no mysql selected")
    else:
        print("Invalid option. Use 'y' to deploy or ignore parameter")

    # flask
    if flask.lower() == "y":
        print("launching flask instance...")
        instance = launch_ec2(images["flask_image"])
        describe_instances(instance, "flask", 1)
    elif flask.lower() == "n":
        print("no flask selected")
    else:
        print("Invalid option. Use 'y' to deploy or ignore parameter")

    # at the end of function, call script or function to update the IP addresses of all servers via the text files

if __name__ == '__main__':
  fire.Fire(cli)


