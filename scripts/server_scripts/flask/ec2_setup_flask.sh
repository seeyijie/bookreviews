#!/bin/bash

server_ip="3.17.147.191"
public_key="flaskserver.pem"
username="ubuntu"

scp -i ~/.ssh/$public_key flask_setup.sh $username@$server_ip:/home/$username
scp -i ~/.ssh/$public_key env_setup.sh $username@$server_ip:/home/$username
ssh -i ~/.ssh/$public_key $username@$server_ip 'sudo ./flask_setup.sh'

