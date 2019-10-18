#!/bin/bash

server_ip="3.18.111.43"
public_key="experimental_instance.pem"
username="ubuntu"

# scp datasets to folder in ec2 instance
scp -i ~/.ssh/$public_key ../../get_data.sh $username@$server_ip:/home/$username
ssh -i ~/.ssh/$public_key $username@$server_ip 'sudo apt-get -y install unzip'
ssh -i ~/.ssh/$public_key $username@$server_ip './get_data.sh'

# scp scripts to folder in ec2 instance
scp -i ~/.ssh/$public_key mongodb_setup.sh $username@$server_ip:/home/$username
ssh -i ~/.ssh/$public_key $username@$server_ip './mongodb_setup.sh'
