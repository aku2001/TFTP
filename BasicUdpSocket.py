import socket
import signal
import sys
from Utilities import DecoderEncoder
# Time Out For Receiving The UDP Package
TIME_OUT = 1

# Let the OS Choose The Port
PORT = 0

# Client IP
UDP_IP = "127.0.0.1" 

# Buffer Size For Receiving
BUFF_SIZE = 1024

class BasicUDPSocket:
    
    def __init__(self):
        # Defaults for UDP
        self.udpSocket = None
        self.uIP = UDP_IP
        self.uPort = PORT

        self.timeout = TIME_OUT
        self.bufferSize = BUFF_SIZE

        # Decoder and Encoder class for type conversion
        self.decoderEncoder = DecoderEncoder()

        # Add Signal Handler 
        # signal.signal(signal.SIGINT,self.signalHandler)
    

    # For Keyboard Interrupt Exit
    def signalHandler(self,signal,frame):
        print("\nProgram Exiting, Thank You For Choosing Us :)")
        sys.exit(0)


    # ---------------------------------------- Functionalities -----------------------------------------------

    # This function is responsible to create a udp socket with given ip and port
    def createUDPSocket(self,ip=UDP_IP,port=PORT,nonblocking=False, timeout = TIME_OUT):
    
        # Create UDP Socket with the given ip and port
        self.uIP = ip
        self.uPort = port
        self.uAdress = (self.uIP,self.uPort)
        self.timeout = timeout

        try:
            # Create the socket and bind it to the given adress to receive messages
            self.udpSocket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
            self.udpSocket.bind(self.uAdress)

            # Set it nonblocking or give a timeout: In non-blocking the socket will not wait for a message
            if(nonblocking):
                self.udpSocket.setblocking(0)
            else:
                self.udpSocket.settimeout(self.timeout)
            
            return True
        
        except Exception as e:
            print(e)
            return False

    # This function is responsible to send udp messages to given ip and port
    # Input: Str, Int, Byte
    def sendUDPMessage(self,msg,ip,port):
        
        self.serverIP = ip
        self.serverPort = port
        self.serverAdress = (ip,port)

        # Encode The Message If It Isn't Encoded
        msg = self.decoderEncoder.convertToByte(msg)

        try:

            # If no udp socket created, create one
            if(self.udpSocket == None):
                self.createUDPSocket()

            # Send the encoded message 
            self.udpSocket.sendto(msg,self.serverAdress)

            return True
        
        except Exception as e:
            print(e)
            return False
            
    # Receive UDP Messages and return adress and the message 
    # Output: Ret,Str, [IP,Port]
    def receiveUDPMessage(self):

        # Check for the socket's availability
        if(self.udpSocket == None):
            self.createUDPSocket()

        # Get the Message and the adress
        try:
            msgAdressPair = self.udpSocket.recvfrom(self.bufferSize)
            msg = msgAdressPair[0]
            adress = msgAdressPair[1]

            # Decode the received message
            msg = self.decoderEncoder.convertToString(msg)
            
            return True, msg, adress
        
        except Exception as e:
            # print(e)
            return False, 0, 0
        
    