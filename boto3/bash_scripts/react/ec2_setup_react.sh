#!/bin/bash
scriptdir="$(dirname "$0")"
cd "$scriptdir"

# import variables server_ip, public_key, username
source ../../config_files/config_react.sh

# check if there is a command line argument
if [ $# -eq 0 ]
    then
    echo "No url specified. Using default dropbox url"
    dropbox_url=https://www.dropbox.com/s/6g4zfii8f0d7yny/bookreviews.zip?dl=0
else
    dropbox_url=$1
fi

scp -o StrictHostKeyChecking=no -i ~/.ssh/$public_key react_setup.sh $username@$server_ip:/home/$username
ssh -o StrictHostKeyChecking=no -i ~/.ssh/$public_key $username@$server_ip "./react_setup.sh $dropbox_url"