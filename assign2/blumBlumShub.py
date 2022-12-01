
from cmath import sqrt
import random


def itsPrim(p):
  gyok = int(p **0.5)
  if p % 4 != 3:
    return False

  for i in range(2,gyok+1):
    if p % i == 0:
      return False
  return True

class BlumBlumShub:
  def __init__(self, seed) -> None:
    self.seed = seed

  def generate(self, l):
    seq = []
    p, q = random.randint(10000,100000), random.randint(10000,100000)

    while True:
      if itsPrim(p):
        if itsPrim(q):
          break
        q += 1
      else:
        if itsPrim(q):
          p +=1
        else:
          q +=1

    n = p*q
    x = (self.seed*self.seed) % n
    for _ in range(l):
      x = (x*x) % n
      seq.append(x%2)

    return bytes(seq)
    
