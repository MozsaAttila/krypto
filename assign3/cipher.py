from solitaire import Solitaire


class Cipher:
  def __init__(self, seed):
    self.seed = seed.copy()

  def encrypt(self, text):
    cipher = Solitaire(self.seed)
    
    seq = cipher.generate(len(text))
    result_int = int.from_bytes(text, byteorder="big") ^ int.from_bytes(seq, byteorder="big")
    return result_int.to_bytes(max(len(text), len(seq)), byteorder="big")

  def decrypt(self, text):
    cipher = Solitaire(self.seed)
    seq = cipher.generate(len(text))
    result_int = int.from_bytes(text, byteorder="big") ^ int.from_bytes(seq, byteorder="big")
    return result_int.to_bytes(max(len(text), len(seq)), byteorder="big")
