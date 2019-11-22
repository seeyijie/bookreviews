#!/bin/bash

# this code should be launched on our local machine and will receive
if [ "$EUID" -eq 0 ] # Root has $EUID = 0
  then echo "Please run this script as non-root (no sudo)."
  exit
fi

# clear flask server
../../config_files/config_mysql.sh
# add server fingerprint to known hosts in local machine
ssh-keygen -R $server_ip
ssh-keyscan -t ecdsa -H $server_ip >> ~/.ssh/known_hosts

# copy helper script over to server and execute it on the server
scp -i ~/.ssh/$public_key helper_mysql.sh $username@$server_ip:/home/$username
ssh -i ~/.ssh/$public_key $username@$server_ip "sudo ./helper_mysql.sh"
ssh-keygen -R $server_ip # remove key at the end (cleanup)
