
from solitaire import Solitaire


class Cipher:
  def __init__(self, generator, seed):
    self.generator = generator
    self.seed = seed.copy()

  def encrypt(self, text):
    if self.generator == "solitaire":
      solitaire = Solitaire(self.seed)
    seq = solitaire.generate(len(text))

    result_int = int.from_bytes(text, byteorder="big") ^ int.from_bytes(seq, byteorder="big")
    return result_int.to_bytes(max(len(text), len(seq)), byteorder="big")

  def decrypt(self, text):
    if self.generator == "solitaire":
      solitaire = Solitaire(self.seed)
    seq = solitaire.generate(len(text))
    result_int = int.from_bytes(text, byteorder="big") ^ int.from_bytes(seq, byteorder="big")
    return result_int.to_bytes(max(len(text), len(seq)), byteorder="big")