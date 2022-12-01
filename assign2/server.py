from socket import *
import threading

serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind(('localhost',1100))

serverSocket.listen(2)

print('Momentarily running')

def threadFunction(connectionSocket, to):
  while True:
    text = connectionSocket.recv(1000000)
    if k == 2:
      connections[to].send(text) 
    if text=="exit".encode():
      connectionSocket.close()
      k -= 1
      return

k = 2
connections = []
connectionSocket,addr = serverSocket.accept()
x1 = threading.Thread(target=threadFunction, args=(connectionSocket,1))
x1.start()
connections.append(connectionSocket)

connectionSocket,addr = serverSocket.accept()
x2 = threading.Thread(target=threadFunction, args=(connectionSocket,0))
x2.start()
connections.append(connectionSocket)

x1.join()
x2.join()
   
serverSocket.close()