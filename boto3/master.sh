#!/bin/bash
keypair=$1
image_id=$2
instance_type=$3

# ==================== Phase 0 - launching of instances ======================
# launch instances
python3 launch_all.py --image=$image_id --keyname=$keypair --instancetype=$instance_type # runs instance and loads

# ===================== Phase 1 - status checks (check if server has finished running user data) =====================
# check status of MySQL server
source ./config_files/config_mysql.sh
echo "Server deployment done. Checking status of mysql."
mysql_server_ip=$server_ip
mysql_public_key=$public_key
mysql_username=$username # NOTE: server username, not mysql database username
# check status and transfer new ip addresses
source ./status_checks/status_check.sh $mysql_server_ip $mysql_public_key $mysql_username

# extract data from mysql server for analytics
(ssh -i ~/.ssh/$mysql_public_key ubuntu@$mysql_server_ip "mysql -u root 50043_DB -e 'select asin, reviewText from reviews' --column-names" > mysql.txt ; sed 's/\t/,/g' mysql.txt > mysql_data.csv ; rm mysql.txt)&

# check status of Mongodb server
source ./config_files/config_mongodb.sh
echo "Checking status of mongodb"
mongo_server_ip=$server_ip
mongo_public_key=$public_key
mongo_username=$username
# check status and transfer new ip addresses
source ./status_checks/status_check.sh $mongo_server_ip $mongo_public_key $mongo_username

# extract data from mongodb server for analytics
(ssh -i ~/.ssh/$mongo_public_key ubuntu@$mongo_server_ip "mongo 50043_db --eval 'db.books_metadata.find({},{asin:1,price:1,_id:0}).forEach(printjson)'" > mongo.txt ; sed '1,4d' mongo.txt > mongo_data.json ; rm mongo.txt) &

# check status of flask
source ./config_files/config_flask.sh
echo "Checking status of flask"
flask_server_ip=$server_ip
flask_public_key=$public_key
flask_username=$username
# check status and transfer new ip addresses
source ./status_checks/status_check.sh $flask_server_ip $flask_public_key $flask_username

# check status of react
source ./config_files/config_react.sh
echo "Checking status of react"
react_server_ip=$server_ip
react_public_key=$public_key
react_username=$username
# check status and transfer new ip addresses
source ./status_checks/status_check.sh $react_server_ip $react_public_key $react_username

# ================== Phase 2 - launch nginx and gunicorn ====================
# start flask server
echo "Starting up gunicorn on flask server"
ssh -i ~/.ssh/$keypair $flask_username@$flask_server_ip "cd /home/ubuntu/bookreviews ; source env/bin/activate ; sudo nohup gunicorn --bind 0.0.0.0:5000 wsgi:app > /dev/null 2>&1 &"

# replace react js config file
echo "Transferring new configuration files for react server"
scp -i ~/.ssh/$keypair config_files/config.js $react_username@$react_server_ip:/home/$react_username/bookreviews/react-end/src/Data
# setup react server to use new IP addresses
ssh -i ~/.ssh/$keypair $react_username@$react_server_ip "cd /home/ubuntu/bookreviews/react-end ; sudo yarn build ; sudo apt-get install -y nginx ; sudo rm /etc/nginx/sites-available/default ; sudo cp /home/ubuntu/bookreviews/boto3/config_files/default /etc/nginx/sites-available ; sudo service nginx start ; sudo service nginx restart"



echo "*************************************************"
echo -e "Deployment done! Thank you for your patience! \nAccess the webpage via the following link: http://$react_server_ip:80"

# ================== Phase 3 - check if data analytics can be run ==================
while  !(test -f mysql_data.csv) && !(test -f mongo_data.json);
do
    sleep 2
done
echo 'Database files are uploaded on local drive'
echo 'You may commence data anlytics'

# TODO: run analytics script