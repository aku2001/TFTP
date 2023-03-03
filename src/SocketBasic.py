import socket
import signal
import sys
from BasicUdpSocket import BasicUDPSocket
from BasicTcpSocket import BasicTCPSocket
    

class BasicSocket:
    def __init__(self) -> None:
        self.basicUdpSocket = BasicUDPSocket()
        self.basicTcpSocket = BasicTCPSocket()