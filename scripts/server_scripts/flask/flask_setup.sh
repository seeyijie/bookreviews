#!/bin/bash

sudo apt-get -y update
sudo apt-get -y upgrade
sudo apt-get install -y python3-pip
sudo apt-get install -y build-essential libssl-dev libffi-dev python-dev
sudo apt-get install -y python3-venv

wget -c https://www.dropbox.com/s/6g4zfii8f0d7yny/bookreviews.zip?dl=0 -O bookreviews.zip
sudo apt-get install -y unzip
unzip bookreviews.zip

cd bookreviews

python3 -m venv env
source env/bin/activate

pip install -r requirements.txt
# TODO: launch flask server
