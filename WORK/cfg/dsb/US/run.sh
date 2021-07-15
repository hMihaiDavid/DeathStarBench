#!/bin/bash

rm -rf res/ 2>/dev/null
mkdir res
rm mangle_map.txt 2>/dev/null

cp *Service.bc test.bc
llvm-dis-9 test.bc > test.ll

python cfg.py test.bc
cd res
for file in *.dot ; do
    dot -Tsvg $file > "$file.svg"  ;
done
