#!/bin/bash

if [ "$EUID" -eq 0 ] # Root has $EUID = 0
  then echo "Please run this script as non-root (no sudo)."
  exit
fi

# clear mysql server
../../config_files/config_mysql.sh
echo "clearing mysql server"
ssh-keygen -R $server_ip
ssh-keyscan -t ecdsa -H $server_ip >> ~/.ssh/known_hosts

ssh -o StrictHostKeyChecking=no -i ~/.ssh/$public_key $username@$server_ip "sudo rm -rf /home/ubuntu/*"
ssh-keygen -R $server_ip # remove key at the end cleanup

# clear mongodb server
../../config_files/config_mongodb.sh
echo "clearning mongodb server"
ssh-keygen -R $server_ip
ssh-keyscan -t ecdsa -H $server_ip >> ~/.ssh/known_hosts

ssh -o StrictHostKeyChecking=no -i ~/.ssh/$public_key $username@$server_ip "sudo rm -rf /home/ubuntu/*"
ssh-keygen -R $server_ip # remove key at the end cleanup

# clear flask server
# echo "clearing flask server"
# ../../config_files/flask.sh
# ssh-keygen -R $server_ip
# ssh-keyscan -t ecdsa -H $server_ip >> ~/.ssh/known_hosts

# ssh -o StrictHostKeyChecking=no -i ~/.ssh/$public_key $username@$server_ip "sudo rm -rf /home/ubuntu/*"
# ssh-keygen -R $server_ip # remove key at the end cleanup