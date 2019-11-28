#!/bin/bash
sudo apt-get -y update
sudo apt-get -y upgrade
# download repository
dropbox_url=https://www.dropbox.com/s/6g4zfii8f0d7yny/bookreviews.zip?dl=0
wget -c $dropbox_url -O bookreviews.zip
sudo apt-get install -y unzip

echo "Unzipping bookzreview.zip"
unzip bookreviews.zip -d "/home/ubuntu/bookreviews"

# installing server software
sudo apt install -y mysql-server
sudo service mysql start

# input mysql user data and create table
sudo mysql -e 'update mysql.user set plugin = "mysql_native_password" where user = "root"'
sudo mysql -e 'create user if not exists "root"@"localhost" identified by ""'
sudo mysql -e 'grant all privileges on *.* to "root"@"localhost" with grant option'
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

# getting data
home="/home/ubuntu"
sudo chown -R ubuntu:ubuntu $home/bookreviews
sudo chmod +x $home/bookreviews/boto3/bash_scripts/get_data.sh

source $home/bookreviews/boto3/bash_scripts/get_data.sh
sudo mysql -u root < $home/bookreviews/boto3/bash_scripts/mysql/initialize_mysql.sql
rm /etc/mysql/mysql.conf.d/mysqld.cnf
mv $home/bookreviews/boto3/config_files/mysqld.cnf /etc/mysql/mysql.conf.d/