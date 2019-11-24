#!/bin/bash
dropbox_url=$1

echo "Downloading bookreviews repository"
wget -c $dropbox_url -O bookreviews.zip
sudo apt-get install -y unzip

sudo mkdir /var/www
sudo gpasswd -a "$USER" www-data
sudo chown -R "$USER":www-data /var/www
find /var/www -type f -exec chmod 0660 {} \;
sudo find /var/www -type d -exec chmod 2770 {} \;

echo "Unzipping bookzreview.zip"
unzip bookreviews.zip -d "/var/www/bookreviews"

# install dependencies for react
echo "Installing yarn"
sudo apt install -y --allow-downgrades libcurl4=7.58.0-2ubuntu3
sudo apt install -y curl
curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | sudo apt-key add -
echo "deb https://dl.yarnpkg.com/debian/ stable main" | sudo tee /etc/apt/sources.list.d/yarn.list
sudo apt-get -y update
sudo apt-get -y upgrade
sudo apt install -y yarn nodejs
cd /var/www/bookreviews/react-end
yarn install


# install dependencies and updates
sudo apt-get install -y python3-pip
sudo apt-get install -y build-essential libssl-dev libffi-dev python-dev
sudo apt-get install -y python3-venv

# installing nginx for react
cd /var/www/bookreviews/react-end
sudo npm install
sudo npm run build
sudo apt-get install nginx

# sudo service nginx start
# sudo service nginx restart # if we make any changes to the config file 



