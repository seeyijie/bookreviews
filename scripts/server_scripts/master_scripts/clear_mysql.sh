#!/bin/bash

if [ "$EUID" -eq 0 ] # Root has $EUID = 0
  then echo "Please run this script as non-root (no sudo)."
  exit
fi

# clear mysql server
source ../config/config_mysql.sh
echo "clearning mysql server"
ssh-keygen -R $server_ip
ssh-keyscan -t ecdsa -H $server_ip >> ~/.ssh/known_hosts

ssh -i ~/.ssh/$public_key $username@$server_ip "sudo rm -rf /home/ubuntu/*"
ssh-keygen -R $server_ip # remove key at the end cleanup