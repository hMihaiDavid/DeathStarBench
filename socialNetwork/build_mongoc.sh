#!/bin/bash
cd /
# Should already be installed
apt-get install cmake libssl-dev libsasl2-dev
wget https://github.com/mongodb/mongo-c-driver/releases/download/1.18.0/mongo-c-driver-1.18.0.tar.gz
tar xzf mongo-c-driver-1.18.0.tar.gz
cd mongo-c-driver-1.18.0
mkdir cmake-build
cd cmake-build
cmake -DENABLE_AUTOMATIC_INIT_AND_CLEANUP=OFF -DCMAKE_BUILD_TYPE=Debug ..
# mongo-c-driver contains a copy of libbson, in case your system does not already have libbson installed
cmake --build .
cmake --build . --target install
