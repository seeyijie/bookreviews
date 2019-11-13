#!/bin/bash

source ../config/config_flask.sh

# add ip address of server to list of known hosts. should remove the need to manually add to trusted hosts
# ssh-keygen -R $server_ip # remove host from host file if it exists
# ssh-keyscan -t ecdsa $server_ip >> /root/.ssh/known_hosts # add ecdsa encrypted fingerprint of server into known hosts
# ssh-keyscan -H $server_ip >> ~/.ssh/known_hosts # add ecdsa encrypted fingerprint of server into known hosts


if [ $# -eq 0 ]
    then
    echo "No url specified. Using default dropbox url"
    dropbox_url=https://www.dropbox.com/s/6g4zfii8f0d7yny/bookreviews.zip?dl=0
else
    dropbox_url=$1
fi

scp -i ~/.ssh/$public_key ../flask/flask_setup.sh $username@$server_ip:/home/$username
scp -i ~/.ssh/$public_key ../flask/env_setup.sh $username@$server_ip:/home/$username
ssh -i ~/.ssh/$public_key $username@$server_ip "sudo ./flask_setup.sh ${dropbox_url}"

