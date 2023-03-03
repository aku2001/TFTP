from BasicUdpSocket import BasicUDPSocket
from TFTP import TFTP, ProtocolSymbols
from ServerInfo import ServerInfo
import time
import multiprocessing
import sys

LOOP_DELAY = 0.01
TRIAL_TIME = 2

def slowDown():
    time.sleep(LOOP_DELAY)


# Handles the file transfer part
def handleServer(msg,ip,port):

    # Create a protocol and socket
    print("Creating another port for TFTP ")
    protocol = TFTP()
    basicUdpSocket = BasicUDPSocket()
    basicUdpSocket.createUDPSocket()

    # Handle the first message //Should be DREQ
    if(protocol.decoderEncoder.convertToString(msg)[0] == ProtocolSymbols.DOWNLOAD_REQ_PACKAGE):
        ret ,resp = protocol.handlePackage(msg)
        print("ret: {}, resp: {}".format(ret,resp))

    else:
        print("Client Handler Requires Req Message. Closing")
        ret = False

    
    i = 0
    endOfFile = False

    while(ret == True and endOfFile == False and i<TRIAL_TIME):

        print("sending msg: {} to : {} : {}".format(resp,ip,port))
        basicUdpSocket.sendUDPMessage(resp,ip,port)
        slowDown()
        succ, msg, addr = basicUdpSocket.receiveUDPMessage()

        if(succ):
            # If message received get the response
            print("Message Received: {}, from: {} : {}".format(msg,ip,port))
            ret ,resp = protocol.handlePackage(msg)
            print("ret: {}, resp: {}".format(ret,resp))

            i = 0

            if(protocol.ackPackage.lineNumber == "0"):
                endOfFile = True
        
        else:
            print("Exiting in " + str(i))
            i+=1
    
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




