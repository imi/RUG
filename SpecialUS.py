from itertools import product
from typing import List, Tuple
# Combinations -> one pair of letters
# Permutations -> pair of letters can be reapeated
# Product -> letters can be repeated

class specialUS():
  def __init__(self, chars: str, pattern: str): 
    self.chars: str = chars
    self.pattern: str = pattern

  def gen(self, flts: int, flt: List[str]) -> List[str]:
    nlst = self.fltrNlst(flt, product(self.chars, repeat=flts))
    flst = []
    for l in nlst:
      ls = []
      at = 0
      for c in flt:
        if "&" in c: 
          ls.append(l[at])
          at += 1
        else: ls.append(c)
      flst.append("".join(ls))
    return flst

  def fltrNlst(self, flt: List, nlst: List) -> List[Tuple]:
    nflt = [i for i in flt if "&" in i]
    nnlst: List = []
    for u in nlst:
      valid: bool = True
      for uu in range(min(len(nflt), len(u))):
        if "&L" in nflt[uu]:
          if not u[uu].isalpha(): 
            valid = False
            break
        if "&N" in nflt[uu]:
          if not u[uu].isdigit(): 
            valid = False
            break
      if valid: nnlst.append(u)
    return nnlst
        

  def new(self) -> List[str]:
    """ 
    &L -> Letter 
    &N -> Number 
    &R -> Random 
    """
    flt: List = []
    flts: int = 0
    at = 0
    for n in range(len(self.pattern)):
      if at > len(self.pattern) - 1: break
      if self.pattern[at] == "&":
        if self.pattern[at+1] == "L": flt.append("&L")
        elif self.pattern[at+1] == "N": flt.append( "&N")
        elif self.pattern[at+1] == "R": flt.append("&R")
        flts += 1
        at += 2
      else: 
        flt.append(self.pattern[at])
        at += 1
    return self.gen(flts, flt)