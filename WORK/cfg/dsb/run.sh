#!/bin/bash

cp UID/run.sh US/run.sh  ; chmod +x US/run.sh
cp UID/run.sh SG/run.sh  ; chmod +x SG/run.sh
#cp UID/run.sh CP/run.sh  ; chmod +x CP/run.sh

cp cfg.py UID/cfg.py
cp cfg.py US/cfg.py
cp cfg.py SG/cfg.py
#cp cfg.py CP/cfg.py

cp ../../../socialNetwork/build/src/UniqueIdService/*.bc UID/
cp ../../../socialNetwork/build/src/UserService/*.bc UID/
cp ../../../socialNetwork/build/src/SocialGraphService/*.bc UID/
#cp ../../../socialNetwork/build/src/ComposePostService/*.bc UID/

cd UID
./run.sh
cd..

cd US
./run.sh
cd ..

cd SG
./run.sh
cd ..

#cd CP
#./run.sh
#cd ..

