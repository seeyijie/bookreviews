#!/bin/bash

sudo apt-get -y update
sudo apt-get -y upgrade

# install dependencies and updates
sudo apt-get install -y python3-pip
sudo apt-get install -y build-essential libssl-dev libffi-dev python-dev
sudo apt-get install -y python3-venv

# download the bookreviews repository
# yijie dropbox test
# wget -c https://www.dropbox.com/s/oq77ssvj8d4cdfn/bookreviews.zip?dl=0 -O bookreviews.zip
# dominic dropbox
wget -c https://www.dropbox.com/s/6g4zfii8f0d7yny/bookreviews.zip?dl=0 -O bookreviews.zip
apt-get install -y unzip
unzip bookreviews.zip -d "/home/ubuntu/bookreviews"

home="/home/ubuntu"
sudo chown -R ubuntu:ubuntu $home/bookreviews

cd "/home/ubuntu/bookreviews" || exit

# create and update virtual environment requirements
sudo python3 -m venv env
source env/bin/activate
sudo python3 -m pip install -r requirements.txt
# sudo nohup gunicorn --bind 0.0.0.0:5000 wsgi:app &

# Resource
# https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-18-04#step-5-%E2%80%94-configuring-nginx-to-proxy-requests
