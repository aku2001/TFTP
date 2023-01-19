from BasicUdpSocket import BasicUDPSocket
import time
from threading import Thread

WANTED_EXECUTION_TIME = 10
DELAY = 0.5

def sendAck(clientIp,clientPort,msg):
    print("Sending ACK for 10 sec")
    
    startTime = time.time()
    lastTime = time.time()
    udpSocket = BasicUDPSocket()
    udpSocket.createUDPSocket()
    
    while(lastTime - startTime < WANTED_EXECUTION_TIME):
        lastTime = time.time()
        udpSocket.sendUDPMessage(msg,clientIp,clientPort)
        time.sleep(DELAY)

    

if __name__ == "__main__":

    serverIP = "127.0.0.1"
    serverPort = 2001

    basicUdpSocket = BasicUDPSocket()
    basicUdpSocket.createUDPSocket(ip=serverIP,port=serverPort)

    while True:
        
        ret,msg,adress = basicUdpSocket.receiveUDPMessage()

        if(ret):
            thread = Thread(target=sendAck, args=(adress[0],adress[1],msg,))
            thread.start()

        