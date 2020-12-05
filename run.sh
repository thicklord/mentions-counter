#!/usr/bin/env bash

cd "${0%/*}"

cd /root/python3_envs/mentions-testing/

DATE=`date +%Y-%m-%d`

./bin/python3 tapi.py >> ./cron-logs/${DATE}-15@cron.log 2>&1


sudo cp -fv ./mentions.json /var/www/html/wp-content/mentions-test.json

