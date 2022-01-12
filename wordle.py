#!/usr/bin/python3

from collections import Counter
from itertools import combinations
import re
import sys

WORDSIZE=5

def sizefilter(dic):
  return filter(lambda w: len(w) == WORDSIZE, dic)

def combos(letters):
  out = []
  letters = list(letters)
  for l in range(min(WORDSIZE, len(letters)), 0, -1):
    for combo in combinations(letters, l):
      out.append(combo)
  return out

def include(letters, dic):
  out = []
  if letters == ".":
    return dic
  for word in dic:
    word_letters = Counter(word)
    for l in letters:
      if l not in word_letters:
        break
    else:
      out.append(word)
  return out

def exclude(letters, dic):
  out = []
  for word in dic:
    if not re.search("[" + letters + "]", word):
      out.append(word)
  return out

def histogram(dic):
  total = Counter()
  for word in dic:
    total += Counter(word)
  return total

def selector(pattern, dic):
  out = []
  pattern = re.sub("_([a-z]+)_", lambda i: "[^" + i.group(1) + "]", pattern)
  pattern = re.compile(pattern)
  for word in dic:
    if pattern.match(word):
      out.append(word)
  return out

dic = set()
with open(sys.argv[1], "r") as f:
  for line in f:
    dic.add(line.strip())
dic = set(sizefilter(dic))

if sys.argv[2] == "x":
  for i in exclude(sys.argv[3], dic):
    print(i)
if sys.argv[2] == "i":
  for i in include(sys.argv[3], dic):
    print(i)
if sys.argv[2] == "c":
  hist = list(histogram(dic).items())
  hist.sort(key=lambda i:i[1], reverse=True)
  for i in hist:
    print(i[1], i[0])
if sys.argv[2] == "ix":
  for i in include(sys.argv[3], exclude(sys.argv[4], selector(sys.argv[5], dic))):
    print(i)
if sys.argv[2] == "ixc":
  hist = list(histogram(include(sys.argv[3], exclude(sys.argv[4], selector(sys.argv[5], dic)))).items())
  hist.sort(key=lambda i:i[1], reverse=True)
  for i in hist:
    print(i[1], i[0])
if sys.argv[2] == "ixcx":
  hist = list(histogram(include(sys.argv[3], exclude(sys.argv[4], selector(sys.argv[5], dic)))).items())
  hist.sort(key=lambda i:i[1], reverse=True)
  for i in hist:
    if i[0] not in sys.argv[4]:
      print(i[1], i[0])
if sys.argv[2] == "ixr":
  filtered_dic = set(include(sys.argv[3], exclude(sys.argv[4], selector(sys.argv[5], dic))))
  if len(filtered_dic)  == 1:
    print("unique solution found: ", list(filtered_dic)[0])
    sys.exit(0)
  def iteritems(double_filter = True):
    hist = list(histogram(filtered_dic.copy()).items())
    hist.sort(key=lambda i:i[1], reverse=True)
    out = {}
    dic_filtered = selector(sys.argv[5], dic)
    if double_filter:
      dic_filtered = exclude(sys.argv[3], dic_filtered)
    for n in range(WORDSIZE, 0, -1):
      for c in combinations(map(lambda i:i[0], hist), n):
        candidates = include("".join(c), dic_filtered.copy())
        for candidate in candidates:
          if candidate not in out:
            out[candidate] = n
          if len(out) > 10:
            return out
    return out
  out = iteritems()
  if out:
    i = 5
    max_combo = 0
    for word, combo in out.items():
      max_combo = max(max_combo, combo)
      print(combo, word)
      i -= 1
      if not i:
        break
    if max_combo <= 2:
      print("no strong downselect candidates, suggesting direct matches:")
      for s in list(filtered_dic)[:5]:
        print(s)
  else:
    print("non-selectable candidates:")
    combo_seen = 0
    for word, combo in iteritems(False).items():
      if combo < combo_seen:
        break
      else:
        combo_seen = combo
      print(word)
