import boto3
import subprocess # to run bash scripts

import boto3
ec2 = boto3.resource('ec2')
keyname = "50043-east1-keypair"

# create a file to store the key locally
outfile = open(f"{keyname}.pem",'w')

# call the boto ec2 function to create a key pair
key_pair = ec2.create_key_pair(KeyName=keyname)

# capture the key and store it in a file
KeyPairOut = str(key_pair.key_material)
print(KeyPairOut)
outfile.write(KeyPairOut)
