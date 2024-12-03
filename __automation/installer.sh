#!/bin/bash

set -e 

# enter sudo user

sudo -i

apt -y update && apt -y install python3-pip

cd /

git clone https://github.com/shomronh/certis.git
echo "clone https://github.com/shomronh/certis.git completed"

cd /certis

git checkout dev
echo "switched to dev branch completed"

BACKEND_URL_VALUE=$(curl -s http://checkip.amazonaws.com)
sed -i "s/^BACKEND_URL=.*/BACKEND_URL=$BACKEND_URL_VALUE/" .env.prod
echo "update BACKEND_URL env value for .env.prod file"

cp /certis/__automation/certis_app.sh /usr/local/bin/certis_app.sh 
cp /certis/__automation/certis.service /lib/systemd/system/certis.service
echo "copied certis_app and certis.service to targets completed"

pip install -r requirements.txt --break-system-packages
echo "install requirements.txt completed"

systemctl start ufw
sudo ufw allow 8080/tcp

systemctl daemon-reload 
systemctl stop certis
systemctl start certis
systemctl enable certis
systemctl status certis






