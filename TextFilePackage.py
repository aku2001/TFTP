
# FILE PACKAGE EXPLANATION --------------------------------------

    # [PT][LN][NC][MSG]

        # [PT]  -> Package Type
        # [LN]  -> Line Number
        # [NC]  -> Number of Characters
        # [MSG] -> Message

# FILE PACKAGE EXPLANATION --------------------------------------


from Utilities import *

# Text File Package is responsible for the text file transfer
class TextFilePackage(Package):
    
    def __init__(self):

        self.packageType = "1"
        self.lineNumber = None
        self.numberOfCharacters = None
        self.lineMsg = None
        self.seperator = ProtocolSymbols.SEPERATOR
        self.msg = None

        # MSG Format
        self.totalMsgLength = 4
        self.packageTypePlace = 0
        self.lineNumberPlace = 1
        self.numberOfCharactersPlace = 2
        self.lineMsgPlace = 3


        self.decoderEncoder = DecoderEncoder()
        
        
    
    # Setters
    def setLineNumber(self,msg):
        self.lineNumber = str(msg)
        
    def setNumberOfCharacters(self,msg):
        self.numberOfCharacters = str(msg)
    
    def setLineMsg(self,msg):
        self.lineMsg = str(msg)
    

    # Abstract Methods

    def createMsg(self):
        
        if(self.checkVariables):
            self.msg = str(self.packageType)

            self.msg += self.seperator
            self.msg += self.lineNumber

            self.msg += self.seperator
            self.msg += self.numberOfCharacters

            self.msg += self.seperator
            self.msg += self.lineMsg

            return self.msg
        
        return None

    def checkVariables(self):
        
        if(self.lineNumber == None):
            return False
        elif(self.numberOfCharacters == None):
            return False
        elif(self.lineMsg == None):
            return False
        
        return True
    
    def parseMsg(self,msg):
        strMsg = self.decoderEncoder.convertToString(msg)
        strMsgList = strMsg.split(self.seperator)

        # print("strMsgList: {}".format(strMsgList))

        if(strMsgList[self.packageTypePlace] != self.packageType):
            print("Wrong Package Type")
            return False
        
        if(len(strMsgList) != self.totalMsgLength ):
            print("Wrong Package Length. The length is : {} but it should be {}".format(len(strMsgList),self.totalMsgLength))
            return False

        self.packageType = strMsgList[self.packageTypePlace]
        self.lineNumber = strMsgList[self.lineNumberPlace]
        self.numberOfCharacters = strMsgList[self.numberOfCharactersPlace]
        self.lineMsg = strMsgList[self.lineMsgPlace]

        return True
        