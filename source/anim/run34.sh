#!/bin/bash
# usage: run34.sh <html> <prefix> <dur>   (v3.4: same baked renderer as v3.2)
cd "$(dirname "$0")"
rm -rf $2l $2d $2.done
python3 render3.py $1 $2l "" 60 $3 2560 > $2l.log 2>&1 &
python3 render3.py $1 $2d "#dark" 60 $3 2560 > $2d.log 2>&1 &
wait
echo done > $2.done
