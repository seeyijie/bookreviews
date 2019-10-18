#!/bin/bash

# this script is to be run to setup the EC2 instance with the requirements for our flask server
sudo apt-get update
sudo apt-get -y upgrade
python -m venv env
source env/bin/activate
pip install -r requirements.txt

# TODO: add flask run command