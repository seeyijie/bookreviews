#!/bin/bash

server_ip="3.14.86.230"
public_key="experimental_instance.pem"
username="ubuntu"

wget -c https://www.dropbox.com/s/6g4zfii8f0d7yny/bookreviews.zip?dl=0 -O bookreviews.zip
sudo apt-get install -y unzip
unzip bookreviews.zip

scp -i ~/.ssh/$public_key flask_setup.sh $username@$server_ip:/home/$username
ssh -i ~/.ssh/$public_key $username@$server_ip 'sudo ./flask_setup.sh'

