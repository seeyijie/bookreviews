#!/bin/bash -X
python3 launch_all.py --image=ami-0d5d9d301c853a04a --keyname=awspem2 # runs instance and loads

source ./config_files/config_mysql.sh
echo "Server deployment done. Installing required software..."
source ./status_checks/status_mysql.sh $server_ip $public_key $username
# add fingerprints to local machine so that there will be no prompts on ssh
# ./config_files/fingerprint_mongodb.sh # adding lines after this file makes this not work...
# source ./config_files/config_mongodb.sh
# ssh-keygen -R $server_ip
# ssh-keyscan -t ecdsa -H $server_ip >> ~/.ssh/known_hosts

# run deployment scripts
# wait
# ./bash_scripts/master_scripts/deploy_mongodb.sh

# after this is run, copy over text files of IP addresses into server