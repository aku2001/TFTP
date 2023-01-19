import socket
import signal
import sys

# Will be implemented later
class BasicTCPSocket:
    
    def __init__(self):
        
        # Default for TCP
        self.tcpSocket = None
        self.tIP = "127.0.0.1"
        self.tPort = 0

        self.bufferSize = 1024
        self.timeout = 0.1

        # Add Signal Handler 
        signal.signal(signal.SIGINT,self.signalHandler)

    def signalHandler(self,signal,frame):
            # For keyboard interruption exit
        print("\nProgram Exiting, Thank You For Choosing Us :)")
        sys.exit(0)