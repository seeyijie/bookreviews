#!/bin/bash

sudo apt-get -y update
sudo apt-get -y upgrade
sudo apt-get install -y python3-pip
sudo apt-get install -y build-essential libssl-dev libffi-dev python-dev
sudo apt-get install -y python3-venv

cd bookreviews

python3 -m venv env
source env/bin/activate

pip install -r requirements.txt
# TODO: launch flask server
