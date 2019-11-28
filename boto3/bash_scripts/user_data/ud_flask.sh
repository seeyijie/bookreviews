<<<<<<< HEAD
#!/bin/bash

## install dependencies and updates
#sudo apt-get install -y python3-pip
#sudo apt-get install -y build-essential libssl-dev libffi-dev python-dev
#sudo apt-get install -y python3-venv
#
## install nginx
#sudo apt update
#sudo apt install -y nginx
#sudo ufw allow 'Nginx HTTP'
#sudo ufw status
#
## download the bookreviews repository
#wget -c https://www.dropbox.com/s/6g4zfii8f0d7yny/bookreviews.zip?dl=0 -O bookreviews.zip
#sudo apt-get install -y unzip
#unzip bookreviews.zip -d "/home/ubuntu/bookreviews"

cd bookreviews

# create and update virtual environment requirements
python3 -m venv env
source env/bin/activate
pip3 install -r requirements.txt

#If you followed the initial server setup guide, you should have a UFW firewall enabled.
# To test the application, you need to allow access to port 5000:
sudo ufw allow 5000

pip3 install gunicorn # in case not installed

gunicorn --bind 0.0.0.0:5000 wsgi:app

deactivate

echo -e "[Unit]\nDescription=Gunicorn instance to serve bookreviews\nAfter=network.target\n\n[Service]\nUser=ubuntu
Group=www-data\nWorkingDirectory=/home/ubuntu/bookreviews
Environment='PATH=/home/ubuntu/bookreviews/env/bin'
ExecStart=/home/ubuntu/bookreviews/env/bin/gunicorn --workers 3 --bind unix:bookreviews -m 007 wsgi:app\n
[Install]
WantedBy=multi-user.target
" | sudo tee /etc/systemd/system/bookreviews.service

sudo systemctl daemon-reload
sudo systemctl start bookreviews
sudo systemctl enable bookreviews
sudo systemctl status bookreviews

echo -e "
server {
    listen 80;
    server_name ec2-3-15-201-236.us-east-2.compute.amazonaws.com www.ec2-3-15-201-236.us-east-2.compute.amazonaws.com;

    location / {
        include proxy_params;
        proxy_pass http://unix:/home/ubuntu/bookreviews/bookreviews;
    }
}" | sudo tee /etc/nginx/sites-available/bookreviews

# Change the config file to allow long domain
# Here the "s" specifies the substitution operation. The "/" are delimiters. The "unix" is the search pattern and the "linux" is the replacement string.
sudo sed -i "s/# server_names_hash_bucket_size 64;/server_names_hash_bucket_size 128;/" /etc/nginx/nginx.conf

sudo ln -s /etc/nginx/sites-available/bookreviews /etc/nginx/sites-enabled

sudo nginx -t # should give a successful message

sudo systemctl restart nginx
sudo ufw delete allow 5000
sudo ufw allow 'Nginx Full'

# Resource
# https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-18-04#step-5-%E2%80%94-configuring-nginx-to-proxy-requests
=======
#!/bin/bash
>>>>>>> 87fc7f39f88a53f4a0b78fc63add1e4b745e0a70
