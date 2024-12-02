#!/bin/bash

#echo "received arguments: $@"
#set -x
#env

export CERTIS_BACKEND_ENV=prod
export CERTIS_PROJECT_DIRECTORY=/certis

python3 /certis/certis_app.py