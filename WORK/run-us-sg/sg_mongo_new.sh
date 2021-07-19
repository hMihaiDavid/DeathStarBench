#!/bin/sh
sudo docker run -p3001:3001 --name social-graph-mongodb  -v "/$(pwd)/config:/config" -d mongo --config /config/mongod_social-graph-service.conf
