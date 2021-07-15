#!/bin/bash
cd /
git clone https://github.com/sewenew/redis-plus-plus.git
cd redis-plus-plus/
mkdir build
cd build
cmake -DREDIS_PLUS_PLUS_USE_TLS=ON -DCMAKE_BUILD_TYPE=Debug ..
# Redis plus plus support is still not included tho, so I had to patch the socialgeraph code, but it links now cause libhiredis_ssl.a is good
make
make install
