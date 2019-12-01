#!/bin/bash
# replace with command line arguments
keypair="50043-keypair"
image_id="ami-0d5d9d301c853a04a"
instance_type="t2.micro"

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

# check status of Mongodb server
source ./config_files/config_mongodb.sh
echo "Checking status of mongodb"
mongo_server_ip=$server_ip
mongo_public_key=$public_key
mongo_username=$username
# check status and transfer new ip addresses
source ./status_checks/status_check.sh $mongo_server_ip $mongo_public_key $mongo_username

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
ssh -i ~/.ssh/$keypair $flask_username@$flask_server_ip "cd /home/ubuntu/bookreviews ; source env/bin/activate ; sudo nohup gunicorn --bind 0.0.0.0:5000 wsgi:app &" &
# replace react js config file
echo "Transferring new configuration files for flask server"
scp -i ~/.ssh/$keypair config_files/config.js $react_username@$react_server_ip:/home/$react_username/bookreviews/react-end/src/Data
# setup react server to use new IP addresses
ssh -i ~/.ssh/$keypair $react_username@$react_server_ip "cd /home/ubuntu/bookreviews/react-end ; yarn build ; apt-get install -y nginx ; rm /etc/nginx/sites-available/default ; cp /home/ubuntu/bookreviews/boto3/config_files/default /etc/nginx/sites-available ; service nginx start ; service nginx restart"

echo "Deployment done! Thank you for your patience! Go to the following link: http://$react_server_ip:80"