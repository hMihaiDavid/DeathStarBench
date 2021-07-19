#!/bin/sh
sudo docker run -p2001:2001 --name user-mongodb -v "/$(pwd)/config:/config" -d mongo --config /config/mongod_user-service.conf
