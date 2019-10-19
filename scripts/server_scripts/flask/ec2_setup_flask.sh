#!/bin/bash

server_ip="3.14.86.230"
public_key="experimental_instance.pem"
username="ubuntu"

echo "Please make sure the EC2 instance has the bookreviews github repo cloned into `/home/ubuntu`"
read -p "Press enter to continue..."

scp -i ~/.ssh/$public_key flask_setup.sh $username@$server_ip:/home/$username
ssh -i ~/.ssh/$public_key $username@$server_ip 'sudo ./flask_setup.sh'

