# this script terminates the 4 instances launched for the production backend
import boto3
from botocore.exceptions import ClientError

ec2 = boto3.resource('ec2')

instance1 = open("metadata/metadata_mysql.txt", "r").read()
instance2 = open("metadata/metadata_mongodb.txt", "r").read()
instance3 = open("metadata/metadata_react.txt", "r").read()
instance4 = open("metadata/metadata_flask.txt", "r").read()

ids = [instance1, instance2, instance3, instance4]

ec2.instances.filter(InstanceIds=ids).stop()
ec2.instances.filter(InstanceIds=ids).terminate()