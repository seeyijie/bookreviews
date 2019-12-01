#!/bin/bash
# ! step 1: wget the dropbox
# wget -c  https://www.dropbox.com/s/oq77ssvj8d4cdfn/bookreviews.zip?dl=0 -O bookreviews.zip
wget -c https://www.dropbox.com/s/6g4zfii8f0d7yny/bookreviews.zip?dl=0 -O bookreviews.zip
sudo apt-get install -y unzip
unzip bookreviews.zip -d "/home/ubuntu/bookreviews"

sudo apt-get update

# ! install nodejs
curl -sL https://deb.nodesource.com/setup_8.x | sudo -E bash -
sudo apt-get install -y nodejs

# ! install yarn
curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | sudo apt-key add -
echo "deb https://dl.yarnpkg.com/debian/ stable main" | sudo tee /etc/apt/sources.list.d/yarn.list
sudo apt update
sudo apt install yarn

home="/home/ubuntu"
sudo chown -R ubuntu:ubuntu $home/bookreviews

cd /home/ubuntu/bookreviews/react-end

# ! install react dependencies with yarn
yarn install
# ! build react app
# yarn build

# # ! install nginx
# apt-get install -y nginx
# rm /etc/nginx/sites-available/default
# cp /home/ubuntu/bookreviews/boto3/config_files/default /etc/nginx/sites-available

# service nginx start
# service nginx restart

