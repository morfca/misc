#!/bin/bash

if [ X$1 == "Xx" ]; then
  grep -v `echo $2 | sed "s,.,-e & ,g"`
elif [ X$1 == "Xi" ]; then
  awk "`echo $2 | sed "s,., /&/ \&\&,g" | sed "s, &&$,,"`"
elif [ X$1 == "Xc" ]; then
  sed "s,.,&\n,g" | grep -v ^$ | sort | uniq -c | sort -rn
fi
