#!/bin/bash
rm test.ll
rm test.bc
rm *.dot
rm *.dot.svg

clang-9 -O0 -g3 -emit-llvm -c test.c
llvm-dis-9 test.bc
python cfg.py test.bc
for file in *.dot; do
    dot -Tsvg $file > "$file.svg";
done
firefox .
