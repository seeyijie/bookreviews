#!/bin/bash

# this code should be launched on our local machine and will receive
if [ "$EUID" -eq 0 ] # Root has $EUID = 0
  then echo "Please run this script as non-root (no sudo)."
  exit
fi

# clear flask server
../../config_files/config_mysql.sh
ssh-keygen -R $server_ip
ssh-keyscan -t ecdsa -H $server_ip >> ~/.ssh/known_hosts

# create a backup in the home folder of the server
ssh -i ~/.ssh/$public_key $username@$server_ip "sudo mysqldump -u root -p 50043_DB > 50043_DB.dump"
ssh-keygen -R $server_ip # remove key at the end cleanup