from BasicUdpSocket import BasicUDPSocket
from TFTP import TFTP, ProtocolSymbols
import time
from ServerInfo import ServerInfo


# TFTP_Client is responsible for asking Text Files to be delivered.
# Getting the text file and showing it on terminal while also saving it to the disk
# Sending Ack packages back to the server to get other parts 

class TFTP_Client:

    def __init__(self):
        
        # This port is reserved for download request
        self.serverIP = ServerInfo.SERVER_IP
        self.serverPort = ServerInfo.SERVER_PORT

        self.clientIP = "127.0.0.1"

        self.udpSocket = BasicUDPSocket()
        self.udpSocket.createUDPSocket(self.clientIP)

        self.downloading = False

        self.protocol = TFTP()
        self.timeOut = 3
    

    # This function is responsible for sending download request to the server
    def sendDownloadRequest(self,fileNumber):
        
        self.protocol.downloadRequestPackage.setFileNumber(fileNumber)
        msg = self.protocol.downloadRequestPackage.createMsg()

        self.udpSocket.sendUDPMessage(msg,self.serverIP,self.serverPort)
        self.downloading = True
    
    def receiveMsg(self):
        ret,msg,addr = self.udpSocket.receiveUDPMessage()

        if(ret):
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
                    self.udpSocket.sendUDPMessage(retMsg,addr[0],addr[1])
                    return True
            
            else:
                print("Package Type Couldn't Be Found Exiting Download")
                self.downloading = False
                return False
        else:
            print("No Package Received Exiting. Server May Not Be Functioning")
            self.downloading = False
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
            fileName = input("Name of the File: ")
            client.protocol.fileNameToWrite = fileName
        
        else:
            client.protocol.isWritingPermitted = False
            
        client.sendDownloadRequest(num)

        while(client.downloading == True):
            ret = client.receiveMsg()
            time.sleep(0.01)
