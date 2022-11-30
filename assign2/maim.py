
from cipher import Cipher


with open("assign2\\bluemereg.png", "rb") as image:
  f = image.read()
b = bytearray(f)

cipher = Cipher("solitaire", [*range(1, 55)])
b = cipher.encrypt(b)
b = cipher.decrypt(b)

with open("assign2\\bluemereg2.png", "wb") as image:
  image.write(b)
