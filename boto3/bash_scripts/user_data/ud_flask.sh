#!/bin/bash

sudo apt-get -y update

# install dependencies and updates
sudo apt-get install -y python3-pip
sudo apt-get install -y build-essential libssl-dev libffi-dev python-dev
sudo apt-get install -y python3-venv

# download the bookreviews repository
wget -c https://50043-bucket.s3.us-east-2.amazonaws.com/bookreviews.zip -O bookreviews.zip
apt-get install -y unzip
unzip bookreviews.zip -d "/home/ubuntu/bookreviews"

home="/home/ubuntu"
sudo chown -R ubuntu:ubuntu $home/bookreviews

cd "/home/ubuntu/bookreviews" || exit

# create and update virtual environment requirements
sudo python3 -m venv env
source env/bin/activate
sudo python3 -m pip install -r requirements.txt
