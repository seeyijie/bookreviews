#!/bin/bash

# this code should be launched on our local machine and will receive
if [ "$EUID" -eq 0 ] # Root has $EUID = 0
  then echo "Please run this script as non-root (no sudo)."
  exit
fi

# clear flask server
source ../config/config_mysql.sh
ssh-keygen -R $server_ip
ssh-keyscan -t ecdsa -H $server_ip >> ~/.ssh/known_hosts

ssh -i ~/.ssh/$public_key $username@$server_ip "sudo mysqldump -u root -p 50043_DB > 50043_DB.dump"
# scp -i ~/.ssh/$public_key $username@$server_ip:/home/$username/50043_DB.dump .
ssh-keygen -R $server_ip # remove key at the end cleanup