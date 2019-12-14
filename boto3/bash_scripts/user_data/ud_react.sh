#!/bin/bash
wget -c https://50043-bucket.s3.us-east-2.amazonaws.com/bookreviews.zip -O bookreviews.zip
sudo apt-get install -y unzip
unzip bookreviews.zip -d "/home/ubuntu/bookreviews"

sudo apt-get update

# install nodejs
curl -sL https://deb.nodesource.com/setup_8.x | sudo -E bash -
sudo apt-get install -y nodejs

# install yarn
curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | sudo apt-key add -
echo "deb https://dl.yarnpkg.com/debian/ stable main" | sudo tee /etc/apt/sources.list.d/yarn.list
sudo apt update
sudo apt install yarn

home="/home/ubuntu"
sudo chown -R ubuntu:ubuntu $home/bookreviews

cd /home/ubuntu/bookreviews/react-end

# install react dependencies with yarn
yarn install
