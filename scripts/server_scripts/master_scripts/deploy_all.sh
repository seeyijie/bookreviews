#!/bin/bash

# sequential deployment of servers on EC2. (Next step: aim to parallelize)
if [ $# -eq 0 ]
    then
    echo "No url specified. Using default dropbox url"
    dropbox_url=https://www.dropbox.com/s/6g4zfii8f0d7yny/bookreviews.zip?dl=0
else
    dropbox_url=$1
fi


# deployment of MongoDB server
echo "************ Deploying MongoDB server **************"
sudo ./../mongodb/ec2_setup_mongodb.sh ${dropbox_url} &

# deployment of MySQL server
echo "************ Deploying MySQL server **************"
sudo ./../mysql/ec2_setup_mysql.sh ${dropbox_url} &

# deployment of Flask server
# echo "************ Deploying Flask server **************"
# sudo ./../flask/ec2_setup_flask.sh ${dropbox_url}
wait
echo "deployment of Servers completed"

# TODO: add "&" to run deployment in background. Prerequisite, remove everything from home folder before doing installation otherwise we will not be able to answer prompts when processes are in background
