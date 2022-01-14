#!/usr/bin/python3

from collections import Counter
from functools import reduce
from itertools import combinations
import re
import sys

WORDSIZE=5

def sizefilter(dic):
  return list(filter(lambda w: len(w) == WORDSIZE, dic))

def include(letters, dic):
  out = dic
  if letters == ".":
    return dic
  for l in letters:
    # the list() call is needed to force the filter to be fully executed immediately
    # this is necessary because 'l' will have a different value if we defer execution
    out = list(filter(lambda w: l in w, out))
  return out

def exclude(letters, dic):
  letters = re.compile("[" + letters + "]")
  return list(filter(lambda i: not letters.search(i), dic))

def histogram(dic):
  total = Counter()
  return reduce(lambda i, j: i + j, map(Counter, dic), Counter())

def selector(pattern, dic):
  out = dic.copy()
  pattern = re.sub("_([a-z]+)_", lambda i: "[^" + i.group(1) + "]", pattern)
  pattern = re.compile(pattern)
  out = list(filter(pattern.match, out))
  return out

def bisect(include_letters, candidates, dic):
  cand_hist = histogram(candidates)
  cand_hist = dict(cand_hist)
  for i in include_letters:
    # remove include letters from the letters being considered. because they're required to be included
    # they will not allow us to narrow the list
    if i in cand_hist:
      del(cand_hist[i])
  bisect_letters = list(cand_hist.items())
  bisect_letters = list(map(lambda i: (i[1], i[0]), bisect_letters))
  bisect_letters.sort(reverse=True)
  for n in range(WORDSIZE, 0, -1):
    for c in combinations(bisect_letters, n):
      bisect_words = include(map(lambda i: i[1], c), dic)
      n = len(bisect_words)
      if n > 0:
        return bisect_words[0]
  return

dic = set()
with open(sys.argv[1], "r") as f:
  for line in f:
    dic.add(line.strip())
dic = set(sizefilter(dic))
include_letters = sys.argv[2]
exclude_letters = sys.argv[3]
selector_pattern = sys.argv[4]
filtered_dic = set(include(include_letters, exclude(exclude_letters, selector(selector_pattern, dic))))
if len(filtered_dic)  == 1:
  print("unique solution found:", list(filtered_dic)[0])
  sys.exit(0)
bisect_result = bisect(include_letters, filtered_dic, dic)
if bisect_result:
  print("bisect candidate:", bisect_result)
  sys.exit(0)
if len(filtered_dic) == 0:
  print("no candidates found, check for user error")
elif len(include_letters) == 5:
  print("ambiguous candidates:")
else:
  print("ambiguous candidates, probable double letter:")
for w in filtered_dic:
  print(w)
sys.exit(0)
