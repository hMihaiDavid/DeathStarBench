#!/bin/sh
# https://hub.docker.com/_/mongo

sudo docker kill user-mongodb 2>/dev/null
sudo docker rm -v user-mongodb
