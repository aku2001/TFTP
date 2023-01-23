from abc import ABC, abstractmethod

# Basic Utilities For TFTP Project


# This class is responsible for encoding and decoding of messages
class DecoderEncoder:
    
    # Converting any data type to string
    def convertToString(self,msg):
        if(isinstance(msg,bytes)):
            return msg.decode()
        
        return str(msg)
    
    # Converting any data type to byte
    def convertToByte(self,msg):
    
        msg = self.convertToString(msg)
        return str.encode(msg)

    
# This class is responsibe for providing the necessary symbols used in TFTP
class ProtocolSymbols:
    
    # Seperator for TFTP
    SEPERATOR = "/;"

    # Seperator used inside the file
    FILE_WORD_SEPERATOR = " "

    # Server send it to tell the file is ended
    END_OF_FILE = "0"

    # Package Types
    TEXT_FILE_PACKAGE = "1"
    DOWNLOAD_REQ_PACKAGE = "2"
    ACK_PACKAGE = "3"

#------------------ Abstract Classes ------------------------------------------------------- 

# For the packages used in the protocol
class Package(ABC):
    
    # This method is responsible to create a msg to send with UDP
    @abstractmethod
    def createMsg(self):
        pass 

    # This method is responsible to parse the incoming str message and change the variables accordingly
    @abstractmethod
    def parseMsg(self,msg):
        pass

    # This method is responsible to check if there are empty variables
    @abstractmethod
    def checkVariables(self):
        pass


# For the protocol

class Protocol(ABC):
    
    # This method is responsible for package handling. It should decide what kind of package it is and call respective functions 
    @abstractmethod
    def handlePackage(self,msg):
        pass