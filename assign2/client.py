from pathlib import Path
from socket import *
import threading
from cipher import Cipher

clientSocket = socket(AF_INET,SOCK_STREAM)
clientSocket.connect(('localhost',1100))

def threadWrite():
  while True:
    imageName = str(Path(__file__).parent) + "\\"
    imageName += input('Please enter image name: ')
    if "exit" in imageName:
      clientSocket.send("exit".encode())
      return
    with open(imageName, "rb") as image:
      f = image.read()
    b = bytearray(f)
 
    b = cipher.encrypt(b)

    clientSocket.send(b)

def threadRead():
  w = 0
  id = clientSocket.recv(1000000).decode()
  while True:
    fromServer = clientSocket.recv(1000000)
    if fromServer == "exit".encode():
      return
    fromServer = cipher.decrypt(fromServer)
    out = str(Path(__file__).parent) + "\\" + str(id) + "ki" + str(w) + ".png"
    w += 1
    with open(out, "wb") as image:
      image.write(fromServer)

with open(str(Path(__file__).parent) + "\\config2.txt", "r") as text:
      f = text.readlines()
text.close()
type = f[0]
if "solitaire" in type:
  key = [int(i) for i in f[1].split(" ")]
  cipher = Cipher("solitaire", key)
else:
  key = [int(i) for i in f[1].split(" ")]
  cipher = Cipher("blumBlumShub", key)

x1 = threading.Thread(target=threadWrite, args=())
x1.start()
x2 = threading.Thread(target=threadRead, args=())
x2.start()

x1.join()
x2.join()

clientSocket.close()