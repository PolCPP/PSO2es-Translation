#!/bin/sh
mkdir -p new/json
find json -maxdepth 1 -name "*.txt" -exec ./jq-tidy.sh {} \;
mv new/json/*.txt json
rm -rf new
