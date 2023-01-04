import random

from utils import bits_to_byte, byte_to_bits, coprime, modinv


def generate_private_key(n = 8):
  w = []
  q = random.randint(2, 10)
  total = 0
  for _ in range(n):
      w.append(q)
      total += q
      q = random.randint(total + 1, 2 * total)
  w = tuple(w)

  r = random.randint(2, q-1)
  while not coprime(q, r):
    r = random.randint(2, q-1)
  
  return (w, q, r)

def create_public_key(private_key):
  return tuple([(private_key[2] * w_i) % private_key[1] for w_i in private_key[0]])
   
def encrypt_mh(message, public_key):
    return [sum([a_i * b_i for (a_i, b_i) in zip(byte_to_bits(byte), public_key)]) for byte in message]  

def decrypt_mh(message, private_key):
    w, q, r = private_key
    s = modinv(r, q)
    plain = []
    for c in message:
        c_ = (c * s) % q
        bits = []
        for w_i in reversed(w):
            if w_i <= c_:
                bits.append(1)
                c_ -= w_i
            else:
                bits.append(0)
        plain.append(bits_to_byte(list(reversed(bits))))
    return bytes(plain)