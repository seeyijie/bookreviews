#!/bin/bash

server_ip="3.16.26.244"
public_key="experimental_instance.pem"
username="ubuntu"

# copy our ssh public key into server for git cloning
scp -i ~/.ssh/$public_key ~/.ssh/id_rsa.pub $username@$server_ip:/home/$username/.ssh # need to figure out how to authenticate github without user credentials
scp -i ~/.ssh/$public_key flask_setup.sh $username@$server_ip:/home/$username
ssh -i ~/.ssh/$public_key $username@$server_ip 'git clone git@github.com:seeyijie/bookreviews.git'
ssh -i ~/.ssh/$public_key $username@$server_ip 'sudo ./flask_setup.sh'

