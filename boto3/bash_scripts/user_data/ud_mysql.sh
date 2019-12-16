#!/bin/bash
sudo apt-get -y update
# sudo apt-get -y upgrade
# download repository
dropbox_url=https://50043-bucket.s3.us-east-2.amazonaws.com/bookreviews.zip
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

sudo service mysql restart

# install virtualenv
sudo apt-get install -y python3-pip
sudo apt-get install -y build-essential libssl-dev libffi-dev python-dev
sudo apt-get install -y python3-venv
sudo python3 -m venv env

# transfer credentials
mkdir /home/ubuntu/.aws
cp /home/ubuntu/bookreviews/credentials/* /home/ubuntu/.aws
sudo chown -R ubuntu:ubuntu /home/ubuntu/.aws

# # TODO: run this part via ssh
# # install virtualenv to run script
# cd "/home/ubuntu/bookreviews" || exit
# python3 -m venv env

# # need to change permissions before running this....
# source env/bin/activate
# pip3 install -r requirements.txt

# # extract data from mysql database and send to s3 bucket
# mysql -u root 50043_DB -e 'select asin, reviewText from reviews' --column-names > mysql.txt
# sed 's/\t/,/g' mysql.txt > mysql_data.csv  
# rm mysql.txt

# cd "/home/ubuntu/bookreviews/boto3"
# python3 boto3/upload_data.py --data_file="mysql_data.csv"