#!/bin/bash

set -e 

# enter sudo user

sudo -i

apt -y update && apt -y install python3-pip

cd /

rm -rf /certis

git clone https://github.com/shomronh/certis.git
echo "clone https://github.com/shomronh/certis.git completed"

cd /certis

git checkout dev
echo "switched to dev branch completed"

chmod +x ./__automation/certis_app.sh

BACKEND_URL_VALUE=$(curl -s http://checkip.amazonaws.com)
sed -i "s/^BACKEND_URL=.*/BACKEND_URL=https://$BACKEND_URL_VALUE:8080/" .env.prod
echo "update BACKEND_URL env value for .env.prod file"

cp -f ./__automation/certis_app.sh /usr/local/bin/certis_app.sh 
cp -f ./__automation/certis.service /lib/systemd/system/certis.service
echo "copied certis_app and certis.service to targets completed"

pip install -r requirements.txt --break-system-packages
echo "install requirements.txt completed"

systemctl start ufw
sudo ufw allow 8080/tcp
echo "firewall configured to use port 8080"

systemctl stop certis
systemctl daemon-reload 
systemctl start certis
systemctl enable certis
systemctl status certis
echo "certis.service has started and enabled"






