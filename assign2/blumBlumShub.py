
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
    [p, q, s] = self.seed
    n = p*q
    x = (s*s) % n
    for _ in range(l):
      x = (x*x) % n
      seq.append(x%2)

    return bytes(seq)

#generate the 2 prim numbers
# p, q = random.randint(10000,100000), random.randint(10000,100000)
# while True:
#  if itsPrim(p):
#    if itsPrim(q):
#      break
#    q += 1
#  else:
#    if itsPrim(q):
#      p +=1
#    else:
#      q +=1
# s = random.randint(1,p*q-1)
# print(p," ",q," ",s)    