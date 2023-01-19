# TEXT FILE TRANSFER PROTOCOL

# MESSAGES:

    # Server Side:
        # [PT: 1] -> Text File package  

    # Client Side:
        # [PT: 2] -> Request to download file [0 is the cfg file]
        # [PT: 3] -> Acknowledgement

# ---------------------------------------------------------------

# FILE PACKAGE EXPLANATION --------------------------------------

    # [PT][LN][NC][MSG]

        # [PT]  -> Package Type
        # [LN]  -> Line Number
        # [NC]  -> Number of Characters
        # [MSG] -> Message

# FILE PACKAGE EXPLANATION --------------------------------------


# DOWNLOAD REQUEST PACKAGE EXPLANATION --------------------------

    # [PT][FN]

        # [PT]  -> Package Type
        # [FN]  -> File Number

# DOWNLOAD REQUEST PACKAGE EXPLANATION --------------------------


# ACKNOWLEDGEMENT PACKAGE EXPLANATION ---------------------------

    # [PT][ALN]

        # [PT]  -> Package Type
        # [ALN] -> Acknowledgement Line Number

# ACKNOWLEDGEMENT PACKAGE EXPLANATION ---------------------------

from Utilities import *
from AcknowledgementPackage import AcknowledgementPackage
from DownoadRequestPackage import DownloadRequestPackage
from TextFilePackage import TextFilePackage






class TFTP(Protocol):

    def __init__(self):

        # Create the packges necessary for the protocol
        self.ackPackage = AcknowledgementPackage()
        self.downloadRequestPackage = DownloadRequestPackage()
        self.textFilePackage = TextFilePackage()

        # Paths and Variables For File IO
        self.folderPath = "Files\\"
        self.listFilePath = "Files\\list.cfg"

        # self.folderPath = ""
        # self.listFilePath = "list.cfg"
        self.wordSeperator = ProtocolSymbols.FILE_WORD_SEPERATOR
        
        self.wantedFileName = None
        self.lastSentLine = None
        self.wantedFileLineList = None

        self.fileNameToWrite = "trial.txt"
        self.isWritingPermitted = False

        # Package Types: 1-> Text File, 2-> Download Request, 3-> Ack Package
        self.ackPackageType = ProtocolSymbols.ACK_PACKAGE
        self.downloadRequestPackageType = ProtocolSymbols.DOWNLOAD_REQ_PACKAGE
        self.textFilePackageType = ProtocolSymbols.TEXT_FILE_PACKAGE

        # Package Types And Their Handlers
        self.functionDict = {
                            self.textFilePackageType: self.textFilePackageHandler,
                            self.downloadRequestPackageType: self.downloadRequestPackageHandler,
                            self.ackPackageType: self.ackPackageHandler
                        }

        # The seperator that will be used to seperate the messages inside the packages
        self.seperator = ProtocolSymbols.SEPERATOR

        # To decode or encode messages
        self.decoderEncoder = DecoderEncoder()
    

    # ------------------------ Abstract Methods ----------------------------------

    def handlePackage(self,msg):

        # Find package type and call their package handlers
        
        strMsg = self.decoderEncoder.convertToString(msg)
        strMsgList = strMsg.split(self.seperator)


        if(len(strMsgList) <= 0):
            return False, 0

        packageType = strMsgList[0]
        
        if(packageType not in self.functionDict.keys()):
            return False
        
        ret,msg = self.functionDict[packageType](msg)
        return ret ,msg



    # ---------------------------------- Package Handlers ----------------------------------


    # This function is responsible for parsing the package. Writing the received lines into a file
    # Creating an ACK package
    def textFilePackageHandler(self,msg):
        
        ret = self.textFilePackage.parseMsg(msg)

        # print("Package Line MSG: {}".format(self.textFilePackage.lineMsg))

        # Can not be parsed
        if(not ret):
            print("The package couldn't be parsed")
            return False, None
        
        # Print and write the message

        if(not self.textFilePackage.lineMsg == ProtocolSymbols.END_OF_FILE):


            if(self.isWritingPermitted):
                msgToWrite = self.textFilePackage.lineMsg + "\n" 
                f = open(self.fileNameToWrite,"a")
                f.write(msgToWrite)

            print(self.textFilePackage.lineMsg)

        # Create Ack Package and return the message
        self.ackPackage.lineNumber = self.textFilePackage.lineNumber
        return True, self.ackPackage.createMsg()
        




    # This function is responsible for reading download request, finding if the file number exist, 
    # Creating a textFilePackage for the first line of the file. The lines are stored in wantedFileLineList
    # The last sent line number is stored in lastSentLine        
     
    def downloadRequestPackageHandler(self,msg):

        ret = self.downloadRequestPackage.parseMsg(msg)

        if(not ret):
            print("Message couldn't be parsed: {}".format(msg))
            return False, None

        # Find the name of the file and store in wantedFileName variable
        fileFound = self.findFileName()
        
        # File Not Found Error
        if(not fileFound):
            print("File doesn't exist in the list")
            return False, None
        

        # Create a textFilePackage
        filePath = self.folderPath + self.wantedFileName
        ret = self.readFile(filePath)

        if(ret):

            wantedLine = self.wantedFileLineList[self.lastSentLine]
            wantedLine = wantedLine.replace("\n", "")
            

            self.textFilePackage.setLineNumber(self.lastSentLine+1)
            self.textFilePackage.setLineMsg(wantedLine)
            self.textFilePackage.setNumberOfCharacters(len(wantedLine))

            return True, self.textFilePackage.createMsg()
    
        return False, None
    

    # Find The Wanted File Name From The List.cfg File
    def findFileName(self):

        try:
            f = open(self.listFilePath,"r")

            fileFound = False

            for line in f:
                line = line.replace("\n", "")
                lineList = line.split(self.wordSeperator)
                
                if(lineList[0] == self.downloadRequestPackage.fileNumber ):
                    self.wantedFileName = lineList[1]
                    self.lastSentLine = 0
                    fileFound = True
                    break
            
            f.close()
            return fileFound
        
        except Exception as e:
            print("File Couldn't Be Found")
            return False
    # This function is responsible for reading a file and turning its lines into a list
    def readFile(self,filePath):
    
        try:

            f = open(filePath,"r")
            self.wantedFileLineList = f.readlines()
            f.close()
            return True
        
        except Exception as e:
            print(e)
            return False

 
    

    # This function is responsible for the parsing of the ACK package. Creating a text File Package for the next line.
    def ackPackageHandler(self,msg):
        
        #Send the next package 
        ret = self.ackPackage.parseMsg(msg)

        if(ret):
            
            # Find which line is received
            self.lastSentLine = int(self.ackPackage.lineNumber)

            # Check if there is a list of lines
            if(self.wantedFileLineList == None):
                filePath = self.folderPath + self.wantedFileName
                ret = self.readFile(filePath)

                if(not ret):
                    return False, None

            # Create a text file package

            if(int(self.lastSentLine) >= len(self.wantedFileLineList)):
                self.textFilePackage.setLineNumber("0")
                self.textFilePackage.setLineMsg("0")
                self.textFilePackage.setNumberOfCharacters(1)

                return True, self.textFilePackage.createMsg()
            
            else:
                
                wantedLine = self.wantedFileLineList[self.lastSentLine]
                wantedLine = wantedLine.replace("\n", "")

                self.textFilePackage.setLineNumber(self.lastSentLine+1)
                self.textFilePackage.setLineMsg(wantedLine)
                self.textFilePackage.setNumberOfCharacters(len(wantedLine))

                return True, self.textFilePackage.createMsg()
        
        return False, None






        

