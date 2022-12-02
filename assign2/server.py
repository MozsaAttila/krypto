from socket import *
import threading

serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind(('localhost',1100))

serverSocket.listen(2)

print('Momentarily running')
k = 2

def threadFunction(connectionSocket, to):
  global k
  connections[to].send(str(to).encode())
  while True:
    text = connectionSocket.recv(1000000)
    if k > 0:
      connections[to].send(text) 
    if text=="exit".encode():
      k -= 1
    if k == 0:
      return


connections = []
connectionSocket,addr = serverSocket.accept()
connectionSocket2,addr2 = serverSocket.accept()
connections.append(connectionSocket)
connections.append(connectionSocket2)
x1 = threading.Thread(target=threadFunction, args=(connectionSocket,1))
x1.start()
x2 = threading.Thread(target=threadFunction, args=(connectionSocket2,0))
x2.start()

x1.join()
x2.join()
connectionSocket.close()
connectionSocket2.close()
   
serverSocket.close()