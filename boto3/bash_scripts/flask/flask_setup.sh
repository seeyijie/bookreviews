#!/bin/bash

# dropbox url is the first command line argument
dropbox_url=$1

# install dependencies for react
echo "Installing yarn"
sudo apt install -y --allow-downgrades libcurl4=7.58.0-2ubuntu3
sudo apt install -y curl
curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | sudo apt-key add -
echo "deb https://dl.yarnpkg.com/debian/ stable main" | sudo tee /etc/apt/sources.list.d/yarn.list
sudo apt-get -y update
sudo apt-get -y upgrade
sudo apt install -y yarn nodejs

# install dependencies and updates
sudo apt-get install -y python3-pip
sudo apt-get install -y build-essential libssl-dev libffi-dev python-dev
sudo apt-get install -y python3-venv

# download the bookreviews repository
wget -c $dropbox_url -O bookreviews.zip
sudo apt-get install -y unzip

# unzip the bookreviews repository
unzip bookreviews.zip -d "/home/ubuntu/bookreviews"
cd bookreviews

# create and update virtual environment requirements
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt

# install react dependencies
cd react-end
yarn install
# launch flask server
# source /home/ubuntu/env_setup.sh
echo 'export FLASK_APP=manage.py' >> ~/.bashrc
echo 'export PORT=80' >> ~/.bashrc
source ~/.bashrc

pip install gunicorn

# flask run
# cd to react-end then sudo yarn start
#CAUTION: if you execute `flask run`, pressing Ctrl+C ends the local ssh connection, not the flask server.
#To end the flask server, ssh into the server and find its process id. by running ps -ef | grep flask, then run sudo kill -9 <process_id>
#Instructions here https://superuser.com/questions/446808/how-to-manually-stop-a-python-script-that-runs-continuously-on-linux
