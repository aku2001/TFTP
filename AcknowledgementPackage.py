
# ACKNOWLEDGEMENT PACKAGE EXPLANATION ---------------------------

    # [PT][ALN]

        # [PT]  -> Package Type
        # [ALN] -> Acknowledgement Line Number

# ACKNOWLEDGEMENT PACKAGE EXPLANATION ---------------------------



from Utilities import *

class AcknowledgementPackage(Package):
    
    def __init__(self):
        
        self.packageType = "3"
        self.lineNumber = None
        self.seperator = ProtocolSymbols.SEPERATOR
        self.msg = None

        # MSG Format
        self.totalMsgLength = 2
        self.packageTypePlace = 0
        self.lineNumberPlace = 1


        self.decoderEncoder = DecoderEncoder()
    
    # Setter

    def setlineNumber(self,msg):
        self.lineNumber = msg
    
    # Abstract Methods

    def createMsg(self):
        
        if(self.checkVariables):
            self.msg = str(self.packageType)

            self.msg += self.seperator
            self.msg += self.lineNumber
            
            return self.msg
        
        return None
    
    def checkVariables(self):
        
        if(self.lineNumber == None):
            return False

        return True
    
    def parseMsg(self,msg):
        strMsg = self.decoderEncoder.convertToString(msg)
        strMsgList = strMsg.split(self.seperator)

        if(strMsgList[self.packageTypePlace] != self.packageType):
            print("Wrong Package Type")
            return False
        
        if(len(strMsgList) != self.totalMsgLength ):
            print("Wrong Package Length")
            return False
        
        self.lineNumber = strMsgList[self.lineNumberPlace] 
        return True
    
        
