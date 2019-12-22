#!/bin/bash

# install dependencies and updates
sudo apt-get install -y python3-pip
sudo apt-get install -y build-essential libssl-dev libffi-dev python-dev
sudo apt-get install -y python3-venv

# download the bookreviews repository
wget -c https://www.dropbox.com/s/6g4zfii8f0d7yny/bookreviews.zip?dl=0 -O bookreviews.zip
sudo apt-get install -y unzip
unzip bookreviews.zip -d "/home/ubuntu/bookreviews"

cd bookreviews

# create and update virtual environment requirements
python3 -m venv env
source env/bin/activate
pip3 install -r requirements_production.txt

#If you followed the initial server setup guide, you should have a UFW firewall enabled.
# To test the application, you need to allow access to port 5000:
sudo ufw allow 5000

pip3 install gunicorn # in case not installed

gunicorn --bind 0.0.0.0:5000 wsgi:app

