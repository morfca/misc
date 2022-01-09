#!/bin/bash

if [ X$1 == "Xx" ]; then
  # exclude letters from candidate words
  grep -v `echo $2 | sed "s,.,-e & ,g"`
elif [ X$1 == "Xi" ]; then
  # require candidate words include letters
  awk "`echo $2 | sed "s,., /&/ \&\&,g" | sed "s, &&$,,"`"
elif [ X$1 == "Xc" ]; then
  # display letter histogram of candidate words
  sed "s,.,&\n,g" | grep -v ^$ | sort | uniq -c | sort -rn | grep -v `echo $2 | sed "s,.,-e & ,g"`
fi
