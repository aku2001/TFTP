from BasicUdpSocket import BasicUDPSocket
from TFTP import TFTP, ProtocolSymbols
import time
from ServerInfo import ServerInfo

TRIAL_TIME = 2

# TFTP_Client is responsible for asking Text Files to be delivered.
# Getting the text file and showing it on terminal while also saving it to the disk
# Sending Ack packages back to the server to get other parts 

class TFTP_Client:

    def __init__(self):
        
        # This port is reserved for download request
        self.serverIP = ServerInfo.SERVER_IP
        self.serverPort = ServerInfo.SERVER_PORT

        self.tmpIP = ServerInfo.SERVER_IP
        self.tmpPort = ServerInfo.SERVER_PORT

        self.clientIP = ServerInfo.CLIENT_IP

        self.udpSocket = BasicUDPSocket()
        self.udpSocket.createUDPSocket(self.clientIP)

        self.downloading = False

        self.protocol = TFTP()
        self.timeOut = 3
    

    # This function is responsible for sending download request to the server
    def sendDownloadRequest(self,fileNumber):
        
        self.protocol.downloadRequestPackage.setFileNumber(fileNumber)
        msg = self.protocol.downloadRequestPackage.createMsg()
        self.protocol.lastMsg  = msg

        self.udpSocket.sendUDPMessage(msg,self.serverIP,self.serverPort)
        self.downloading = True

        self.tmpPort = ServerInfo.SERVER_PORT
        self.tmpIP = ServerInfo.SERVER_IP
    
    def receiveMsg(self):

        # time.sleep(0.5)
        ret,msg,addr = self.udpSocket.receiveUDPMessage()
        i=0

        while(not ret and i< TRIAL_TIME):
            print("Trying to get connection, Sending the message again")
            self.udpSocket.sendUDPMessage(self.protocol.lastMsg,self.tmpIP,self.tmpPort)

            time.sleep(0.05)
            ret,msg,addr = self.udpSocket.receiveUDPMessage()

            i += 1

        if(ret):
            self.tmpIP = addr[0]
            self.tmpPort = addr[1]
            # print("Received message client: ",msg)
            ret,retMsg = self.protocol.handlePackage(msg)
            
            if(ret):

                # Check if the received text is EOF
                if(self.protocol.ackPackage.lineNumber == ProtocolSymbols.END_OF_FILE):
                    self.udpSocket.sendUDPMessage(retMsg,addr[0],addr[1])
                    print("Download Completed Succesfully")
                    self.downloading = False
                    return True


                # If There is a return message send it to the server
                if( retMsg != None):
                    # print("Ret message client: ",retMsg)
                    self.udpSocket.sendUDPMessage(retMsg,addr[0],addr[1])
                    return True
            
            else:
                print("Package Type Couldn't Be Found")
                return False
        else:
            print("No Package Received Exiting. Server May Not Be Functioning")
            return False
    
if __name__ == "__main__":

    client = TFTP_Client()
    print("WELCOME TO TEXT FILE DOWNLOADER")

    # Get the list.cfg
    client.sendDownloadRequest(0)

    while(client.downloading == True):
        ret = client.receiveMsg()
        time.sleep(0.01)
    

    while True:

        # Ask For which file it wants to download

        num = input("Which File Do You Want to Download (press 0 to downlaod the list): ")

        ret = input("Would You Like to Download the File (Y/N): ")

        if(ret == "Y" or ret == "y"):
            client.protocol.isWritingPermitted = True
            fileName = input("Name of the File (with .txt prefix): ")

            if(fileName[-4:] != ".txt"):
                fileName += ".txt"
                
            client.protocol.fileNameToWrite = fileName
        
        else:
            client.protocol.isWritingPermitted = False
            
        client.sendDownloadRequest(num)

        tiral = 0
        while(client.downloading == True):
            ret = client.receiveMsg()

            if(ret):
                trial = 0
            else:
                print("Sending The Message Again")
                trial += 1
            
            if(trial >= TRIAL_TIME):
                print("Download Canceled")
                client.downloading = False

            time.sleep(0.01)
