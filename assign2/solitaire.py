

class Solitaire:
  def __init__(self, seed) -> None:
    self.seed = seed.copy()

  def generate(self, n):
    seq = []

    while len(seq) < n:
      #a
      indexOfWhiteJoker = self.seed.index(53)
      if indexOfWhiteJoker == 53:
        self.seed.insert(1, self.seed[indexOfWhiteJoker])
        self.seed.pop(indexOfWhiteJoker+1)
        indexOfWhiteJoker = 1
      else:
        self.seed[indexOfWhiteJoker], self.seed[indexOfWhiteJoker + 1] = self.seed[indexOfWhiteJoker + 1], self.seed[indexOfWhiteJoker]
        indexOfWhiteJoker = indexOfWhiteJoker + 1
      #b
      indexOfBlackJoker = self.seed.index(54)
      if indexOfBlackJoker < 52:
        self.seed[indexOfBlackJoker], self.seed[indexOfBlackJoker + 2] = self.seed[indexOfBlackJoker + 2], self.seed[indexOfBlackJoker]
        indexOfBlackJoker = indexOfBlackJoker + 2
      elif indexOfBlackJoker == 53:
        self.seed.inser(2, self.seed[indexOfBlackJoker])
        self.seed.pop(indexOfBlackJoker + 1)
        indexOfBlackJoker = 2
      else:
        self.seed.insert(1, self.seed[indexOfBlackJoker])
        self.seed.pop(indexOfBlackJoker + 1)
        indexOfBlackJoker = 1
      #c
      joker_1, joker_2 = min(indexOfBlackJoker, indexOfWhiteJoker), max(indexOfBlackJoker, indexOfWhiteJoker)
      self.seed = self.seed[joker_2+1:] + self.seed[joker_1:joker_2+1] + self.seed[:joker_1]
      #d
      cardsToCount = min(self.seed[-1], 53)
      self.seed[:-1] = self.seed[cardsToCount:-1] + self.seed[:cardsToCount]
      #e
      if self.seed[0] < 53:
          seq.append(self.seed[self.seed[0]])
    
    return bytes(seq)

#generate seed
#import random
#for i in random.sample( [*range(1, 55)],54):
#  print(i,end=" ")

    