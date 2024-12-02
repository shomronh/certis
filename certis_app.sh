#!/bin/bash

#echo "received arguments: $@"
#set -x
#env

export CERTIS_BACKEND_ENV=prod

python3 /certis/certis_app.py