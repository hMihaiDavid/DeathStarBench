#!/bin/sh
# https://hub.docker.com/_/mongo

sudo docker kill social-graph-mongodb 2>/dev/null
sudo docker rm -v social-graph-mongodb
