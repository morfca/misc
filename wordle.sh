#!/bin/bash

VALID_WORD_RE="^.....$"

function exclude () {
  grep -v `echo $1 | sed "s,.,-e & ,g"`
}

function include () {
  awk "`echo $1 | sed "s,., /&/ \&\&,g" | sed "s, &&$,,"`"
}

function histogram () {
  sed "s,.,&\n,g" | grep -v ^$ | sort | uniq -c | sort -rn
}

SELECTOR="` echo "${4}" | sed "s,_\([a-z][a-z]*\)_,[^\1],g" `"

if [ X$1 == "Xx" ]; then
  # exclude letters from candidate words
  grep $VALID_WORD_RE | ( exclude $2 )
elif [ X$1 == "Xi" ]; then
  # require candidate words include letters
  grep $VALID_WORD_RE | ( include $2 )
elif [ X$1 == "Xc" ]; then
  # display letter histogram of candidate words
  grep $VALID_WORD_RE | ( histogram ) | ( exclude $2 )
elif [ X$1 == "Xixc" ]; then
  grep $VALID_WORD_RE | ( include $2 ) | ( exclude $3 ) | grep "^${SELECTOR}$" | ( histogram ) | ( exclude $2 )
elif [ X$1 == "Xix" ]; then
  grep $VALID_WORD_RE | ( include $2 ) | ( exclude $3 ) | grep "^${SELECTOR}$"
fi
