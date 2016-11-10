#!/bin/sh
cat $1 | jq --tab -r -M '.' | cat > new/$1
