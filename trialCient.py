from BasicUdpSocket import BasicUDPSocket
import time
from threading import Thread
import sys

exitThread = False

def receiveMessageThread(udpSocket):
    global exitThread
    while not exitThread:
        ret,msg,addr = udpSocket.receiveUDPMessage()
        if(ret):
            print(msg)
        
        time.sleep(0.1)
    
    print("Exited")


if __name__ == "__main__":

    serverIP = "127.0.0.1"
    serverPort = 2001

    basicUdpSocket = BasicUDPSocket()
    basicUdpSocket.createUDPSocket()

    thread = Thread(target=receiveMessageThread,args= (basicUdpSocket,))
    thread.daemon = False
    thread.start()
    msg = "hello"

    while msg != "exit":

        try:
            msg = input("Enter something to send to the server: ")
            basicUdpSocket.sendUDPMessage(msg,serverIP,serverPort)
        except KeyboardInterrupt:
            exitThread = True
            msg = "exit"

            
    print("Exited")
    exitThread = True
    sys.exit()

        

        