#!/bin/bash
cd /
apt-get update && apt-get install -y lsb-release wget software-properties-common apt-transport-https && apt-get clean all
wget https://apt.llvm.org/llvm.sh
chmod +x llvm.sh
./llvm.sh 9
