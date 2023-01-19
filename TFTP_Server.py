from BasicUdpSocket import BasicUDPSocket
from TFTP import TFTP, ProtocolSymbols
from ServerInfo import ServerInfo
import time
import multiprocessing
import sys

LOOP_DELAY = 0.01

def slowDown():
    time.sleep(LOOP_DELAY)


# Handles the file transfer part
def handleServer(msg,ip,port):

    # Create a protocol and socket
    protocol = TFTP()
    basicUdpSocket = BasicUDPSocket()
    basicUdpSocket.createUDPSocket()

    # Handle the first message //Should be DREQ
    ret ,resp = protocol.handlePackage(msg)
    endOfFile = False

    print("ret: {}, resp: {}".format(ret,resp))

    while(ret == True and endOfFile == False):

        basicUdpSocket.sendUDPMessage(resp,ip,port)
        succ, msg, addr = basicUdpSocket.receiveUDPMessage()
        print("Message Received: {}".format(msg))

        if(succ):
            # If message received get the response
            ret ,resp = protocol.handlePackage(msg)
            print("ret: {}, resp: {}".format(ret,resp))


            if(protocol.ackPackage.lineNumber == "0"):
                endOfFile = True
        
        slowDown()
    
    if(endOfFile):
        print("File Sent Succesfully")
    else:
        print("Error in Server")
        
        


if __name__ == "__main__":
    print("Welcome to the Server Side of the Project")
    serverUdpSocket = BasicUDPSocket()
    serverIP = ServerInfo.SERVER_IP
    serverPort = ServerInfo.SERVER_PORT
    serverUdpSocket.createUDPSocket(ip=serverIP,port=serverPort)
    processList = []
 
    while True:
        
        try:
            ret,msg,addr =  serverUdpSocket.receiveUDPMessage()

            if(ret):
                print("Message received: {}, from: {} : {}".format(msg,addr[0],addr[1]))
                process = multiprocessing.Process(target=handleServer, args=(msg,addr[0],addr[1],))
                process.start()
                processList.append(process)
        
        except KeyboardInterrupt:
            
            # Kill the processes
            for process in processList:
                if(process.is_alive()):
                    process.terminate()    

            # Exit the system
            print("Closing Server")
            sys.exit()            




