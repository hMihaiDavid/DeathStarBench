#!/bin/bash
rm -rf build 2>/dev/null
sudo docker cp dsb:/social-network-microservices/build ./build
cd build
sudo chown -R klee:klee .
cd ..
