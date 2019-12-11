#!/bin/bash

#overview
#ssh into each database instance and pipe the outputs to a text file


#mysql
source ./config_files/config_mysql.sh
echo "Exporting mysql data"
mysql_server_ip=$server_ip
mysql_public_key=$public_key
ssh -i ~/.ssh/$mysql_public_key ubuntu@$mysql_server_ip "mysql -u root 50043_DB -e 'select asin, reviewText from reviews' --column-names" > mysql.txt
echo "Writing data to mysql_data.csv"
sed 's/\t/,/g' mysql.txt > mysql_data.csv  
rm mysql.txt

#mongo
source ./config_files/config_mongodb.sh
echo "Exporting mongo data"
mongo_server_ip=$server_ip
mongo_public_key=$public_key
ssh -i ~/.ssh/$mongo_public_key ubuntu@$mongo_server_ip "mongo 50043_db --eval 'db.books_metadata.find({},{asin:1,price:1,_id:0}).forEach(printjson)'" > mongo.txt
echo "Writing data to mongo_data.json"
sed '1,4d' mongo.txt > mongo_data.json
rm mongo.txt

echo "Done"

