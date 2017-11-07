#!/bin/sh
mkdir -p new/json
find $@ -maxdepth 1 -name "*.txt" -exec ./jq-tidy.sh {} \;
rm -rf new
