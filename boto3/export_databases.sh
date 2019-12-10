#!/bin/bash

#overview
#ssh into each database instance and execute export
#scp files over to local computer

source ./config_files/config_mysql.sh
echo "Exporting mysql data"
mysql_server_ip=$server_ip
mysql_public_key=$public_key
ssh -i ~/$mysql_public_key ubuntu@$mysql_server_ip "mysqldump -u root 50043_DB > mysql_data.sql"
scp -i ~/$mysql_public_key ubuntu@$mysql_server_ip:/home/ubuntu/mysql_data.sql . 



source ./config_files/config_mongodb.sh
echo "Exporting mongo data"
mongo_server_ip=$server_ip
mongo_public_key=$public_key
ssh -i ~/$mongo_public_key ubuntu@$mongo_server_ip "mongoexport -d 50043_db -c books_metadata -o mongo_data.json"
scp -i ~/$mongo_public_key ubuntu@$mongo_server_ip:/home/ubuntu/mongo_data.json . 

echo "Done"

