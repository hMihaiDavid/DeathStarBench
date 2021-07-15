#!/bin/bash
cd /
git clone https://github.com/redis/hiredis
cd hiredis
make USE_SSL=1
make install USE_SSL=1
