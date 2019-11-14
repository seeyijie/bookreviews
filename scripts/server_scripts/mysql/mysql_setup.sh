#!/bin/bash

# dropbox url is the first command line argument
dropbox_url=$1

echo "Installing MySQL"
sudo apt-get -y update
sudo apt-get -y upgrade
sudo apt install -y mysql-server

# start mysql in the background
echo "Starting MySQL service"
sudo service mysql start

# need to explicitly grant access to "root" user
# TODO: might change the root host connection from "%" to "localhost" to prevent external connections to root
sudo mysql -e 'update mysql.user set plugin = "mysql_native_password" where user = "root"'
sudo mysql -e 'create user if not exists "root"@"%" identified by ""'
sudo mysql -e 'grant all privileges on *.* to "root"@"%" with grant option'
sudo mysql -e 'flush privileges'
sudo service mysql restart

MAINDB="50043_DB"
PASSWDDB="password"

# creates a database and user named 50043_DB and gives the user all permissions for the 50043_DB database
# this user is contained withing the 50043_DB database
mysql -e "CREATE DATABASE IF NOT EXISTS ${MAINDB} /*\!40100 DEFAULT CHARACTER SET utf8 */;"
mysql -e "CREATE USER IF NOT EXISTS ${MAINDB}@'%' IDENTIFIED BY '${PASSWDDB}';"
mysql -e "GRANT ALL PRIVILEGES ON ${MAINDB}.* TO '${MAINDB}'@'%';"
mysql -e "FLUSH PRIVILEGES;"

echo "Downloading bookreviews repository"
wget -c $dropbox_url -O bookreviews.zip
sudo apt-get install -y unzip

echo "Unzipping bookzreview.zip"
unzip bookreviews.zip -d "/home/ubuntu/bookreviews"


