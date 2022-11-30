from socket import *
import threading
from cipher import Cipher

clientSocket = socket(AF_INET,SOCK_STREAM)
clientSocket.connect(('localhost',1100))

def threadWrite():
  while True:
    imageName = "assign2\\"
    imageName += input('Please enter image name: ')
    if imageName == "assign2\\exit":
      clientSocket.send("exit".encode())
      break
    with open(imageName, "rb") as image:
      f = image.read()
    b = bytearray(f)
 
    b = cipher.encrypt(b)

    clientSocket.send(b)

def threadRead():
  write = 0
  while True:
    fromServer = clientSocket.recv(1000000)
    if fromServer == "exit".encode():
      print("please write exit, because the mate has left the chat!")
      break
    fromServer = cipher.decrypt(fromServer)
    out = "assign2\\ki" + str(write) + ".png"
    write += 1
    with open(out, "wb") as image:
      image.write(fromServer)


cipher = Cipher("solitaire", [*range(1, 55)])
x1 = threading.Thread(target=threadWrite, args=())
x1.start()
x2 = threading.Thread(target=threadRead, args=())
x2.start()

x1.join()
x2.join()

clientSocket.close()