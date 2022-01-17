#!/usr/bin/python3

from collections import Counter
from functools import reduce
from itertools import combinations
import random
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

def bisect(include_letters, ans, dic):
  cand_hist = histogram(ans)
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
      if len(bisect_words) > 0:
        return bisect_words[0]
  return

def guess(answer_word, guess_word):
  incl = set()
  excl = set()
  pattern = ""
  for gl in guess_word:
    if gl in answer_word:
      incl.add(gl)
    else:
      excl.add(gl)
  for i in range(0, len(guess_word)):
    l = guess_word[i]
    if l == answer_word[i]:
      pattern += l
    elif l in incl:
      pattern += "_{}_".format(l)
    else:
      pattern += "."
  return "".join(incl), "".join(excl), pattern

def merge_patterns(pattern1, pattern2):
  out = []
  field_re = re.compile("((\.)|(_[a-z]+_)|([a-z]))")
  fields1 = list(map(lambda i: i.groups()[1:], field_re.finditer(pattern1)))
  fields2 = list(map(lambda i: i.groups()[1:], field_re.finditer(pattern2)))
  for i in range(0, len(fields1)):
    if fields1[i][2] or fields2[i][2]:
      out.append(fields1[i][2] or fields2[i][2])
    elif fields1[i][1] or fields2[i][1]:
      letters = set()
      if fields1[i][1]:
        letters |= set(iter(fields1[i][1].strip("_")))
      if fields2[i][1]:
        letters |= set(iter(fields2[i][1].strip("_")))
      out.append("_{}_".format("".join(letters)))
    else:
      out.append(".")
  return "".join(out)

def step(dict_file, ans_file, include_letters, exclude_letters, selector_pattern):
  dic = set()
  ans = set()
  with open(dict_file, "r") as f:
    for line in f:
      dic.add(line.strip())
  with open(ans_file, "r") as f:
    for line in f:
      ans.add(line.strip())
  dic = set(sizefilter(dic))
  ans = set(sizefilter(ans))
  filtered_ans = set(include(include_letters, exclude(exclude_letters, selector(selector_pattern, ans))))
  if len(filtered_ans)  == 1:
    print("unique solution found:", list(filtered_ans)[0])
    return "U", list(filtered_ans)[0]
  bisect_result = bisect(include_letters, filtered_ans, dic)
  if bisect_result:
    print("bisect candidate:", bisect_result)
    return "B", bisect_result
  if len(filtered_ans) == 0:
    print("no candidates found, check for user error")
    sys.exit(1)
  elif len(include_letters) == 5:
    print("ambiguous candidates:", ", ".join(filtered_ans))
  else:
    print("ambiguous candidates, probable double letter:", ", ".join(filtered_ans))
  return "A", filtered_ans

if len(sys.argv) == 5:
  soln = sys.argv[3]
  starter = sys.argv[4]
  print("answer:", soln)
  print("starting guess:", starter)
  state = "S"
  incl, excl, pattern = guess(soln, starter)
  print("guess results:", "i:"+incl, "x:"+excl, "p:"+pattern)
  print()
  iterations = 1
  while state != "U":
    iterations += 1
    state, next_word = step(sys.argv[1], sys.argv[2], incl, excl, pattern)
    if state == "A":
      next_word = random.choice(list(next_word))
    new_incl, new_excl, newpattern = guess(soln, next_word)
    pattern = merge_patterns(newpattern, pattern)
    incl = "".join(set(iter(incl)) | set(iter(new_incl)))
    excl = "".join(set(iter(excl)) | set(iter(new_excl)))
    if state == "U":
      break
    print("guess results:", "i:"+new_incl, "x:"+new_excl, "p:"+pattern)
    print("total clues:", "i:"+incl, "x:"+excl, "p:"+pattern)
    print()
  print("iterations required", iterations)
else:
  step(*sys.argv[1:6])
