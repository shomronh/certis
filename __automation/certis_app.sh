#!/bin/bash

#echo "received arguments: $@"
#set -x
#env

BACKEND_URL_VALUE=$(curl -s http://checkip.amazonaws.com)

# replace dots of IP address with dashs
BACKEND_URL_VALUE=$(echo "$BACKEND_URL_VALUE" | sed 's/\./-/g')


sed -i "s|^BACKEND_URL=.*|BACKEND_URL=http://ec2-$BACKEND_URL_VALUE.us-west-2.compute.amazonaws.com:8080|" .env.prod
echo "update BACKEND_URL env value for .env.prod file"

export CERTIS_BACKEND_ENV=prod

python3 /certis/certis_app.py