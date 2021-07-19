#!/bin/sh
# https://hub.docker.com/_/mongo

sudo docker kill social-graph-redis 2>/dev/null
sudo docker rm -v social-graph-redis
