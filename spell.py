#!/usr/bin/env python
# -*- coding: utf-8 -*-
from collections import defaultdict
import re

def words(text): return re.findall('[a-z]+', text.lower())

def words_and_bigrams(text):
  all_words = words(text)
  bigrams = [ ' '.join(all_words[i:i+2]) for i in range(len(all_words)-1) ]
  return all_words + bigrams

def train(features):
    model = defaultdict(lambda: 1)
    for f in features:
        model[f] += 1
    return model

NWORDS = train(words_and_bigrams(file('big.txt').read()))

alphabet = 'abcdefghijklmnopqrstuvwxyz\''

def edits1(word):
   splits     = [(word[:i], word[i:]) for i in range(len(word) + 1)]
   deletes    = [a + b[1:] for a, b in splits if b]
   transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b)>1]
   replaces   = [a + c + b[1:] for a, b in splits for c in alphabet if b]
   inserts    = [a + c + b     for a, b in splits for c in alphabet]
   return set(deletes + transposes + replaces + inserts)

def known_edits2(word):
    return set(e2 for e1 in edits1(word) for e2 in edits1(e1) if e2 in NWORDS)

def known(words): return set(w for w in words if w in NWORDS)

# list all possible fusion error candidate
def fusions_edit(word):
   word        = word.replace(' ', '')
   splits     = [(word[:i], word[i:]) for i in range(1, len(word))]
   fusions    = [(a+' '+b) for a, b in splits if a in NWORDS and b in NWORDS]
   if word in NWORDS:
      fusions += [word]
   return fusions

def correct(word):
    candidates = known([word]) or fusions_edit(word) or known(edits1(word)) or known_edits2(word) or [word]
    return max(candidates, key=NWORDS.get)

if __name__ == '__main__':
    examples = ['taketo', 'mor efun', 'with out']
    for example in examples:
        print example, '->', correct(example)