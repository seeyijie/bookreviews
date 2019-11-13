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
# scp -i ~/.ssh/$public_key ../backup_scripts/50043_DB.dump $username@$server_ip:/home/$username
scp -i ~/.ssh/$public_key helper_mysql.sh $username@$server_ip:/home/$username
ssh -i ~/.ssh/$public_key $username@$server_ip "sudo ./helper_mysql.sh"
ssh-keygen -R $server_ip # remove key at the end (cleanup)
