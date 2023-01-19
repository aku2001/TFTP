

# DOWNLOAD REQUEST PACKAGE EXPLANATION --------------------------

    # [PT][FN]

        # [PT]  -> Package Type
        # [FN]  -> File Number

# DOWNLOAD REQUEST PACKAGE EXPLANATION --------------------------




from Utilities import *

class DownloadRequestPackage(Package):
    
    def __init__(self):
        
        self.packageType = "2"
        self.fileNumber = None
        self.seperator = ProtocolSymbols.SEPERATOR
        self.msg = None

        # MSG Format
        self.totalMsgLength = 2
        self.packageTypePlace = 0
        self.fileNumberPlace = 1


        self.decoderEncoder = DecoderEncoder()
    
    
    # Setters
    def setFileNumber(self,msg):
        self.fileNumber = str(msg)
    
    # Abstract Methods
    def createMsg(self):
        
        if(self.checkVariables):
            self.msg = str(self.packageType)

            self.msg += self.seperator
            self.msg += self.fileNumber
            
            return self.msg
        
        return None
    
    def checkVariables(self):
        
        if(self.fileNumber == None):
            return False

        return True
    
    def parseMsg(self,msg):
        strMsg = self.decoderEncoder.convertToString(msg)
        strMsgList = strMsg.split(self.seperator)

        # print("msgList: {}".format(strMsgList))

        if(strMsgList[self.packageTypePlace] != self.packageType):
            print("Wrong Package Handler")
            return False
        
        if(len(strMsgList) != self.totalMsgLength ):
            print("Package Length Faulty")
            return False
        
        self.fileNumber = strMsgList[self.fileNumberPlace] 
        return True

    