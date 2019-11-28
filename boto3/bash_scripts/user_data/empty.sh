#!/bin/bash

3.134.90.197 - react

ssh -vvv -i ~/.ssh/awspem2.pem ubuntu@3.134.90.197

18.191.2.8 - blank


ssh -vvv -i ~/.ssh/awspem2.pem ubuntu@18.191.2.8

! step 1: wget the dropbox

dropbox_url=https://www.dropbox.com/s/6g4zfii8f0d7yny/bookreviews.zip?dl=0
wget -c $dropbox_url -O bookreviews.zip

sudo apt-get update

! install nodejs
curl -sL https://deb.nodesource.com/setup_8.x | sudo -E bash -
sudo apt-get install -y nodejs

cd react-end/

! install yarn
curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | sudo apt-key add -
echo "deb https://dl.yarnpkg.com/debian/ stable main" | sudo tee /etc/apt/sources.list.d/yarn.list
sudo apt update
sudo apt install yarn

! install react dependencies with yarn
yarn install

! build react app
yarn build

! install nginx
apt-get install -y nginx

rm /etc/nginx/sites-available/default
mv /home/ubuntu/bookreviews/boto3/config_files/default /etc/nginx/sites-available/default

service nginx start