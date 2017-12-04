#!/bin/sh
mkdir -p new/json
find $@ -maxdepth 1 -name "*.txt" -exec ./_sh/jq-tidy.sh {} \;
rm -rf new
