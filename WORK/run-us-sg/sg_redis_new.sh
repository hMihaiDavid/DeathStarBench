#!/bin/sh
sudo docker run -p3002:3002 --name social-graph-redis  -v "/$(pwd)/config:/config" -d redis /config/redis_social-graph-service.conf
