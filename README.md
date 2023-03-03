TFTP: Text File Transfer Protocol

1.	Introduction:
This project is the lab work for the computer communication course. For the project there are certain requirements and tasks that are needed to be handled and be tested. It is required to create a file transfer protocol by using Python or Java. Because of the implementation ease, Python is chosen. In the implementation, the task is divided in two: Client side and server side. The server side is responsible for containing some files and one specific file that has the names of every file (list.cfg). The server is also responsible for sending the file to the client when asked. The client side of the project is responsible for communicating with the users by an interface and convert the requests into action. The client side of the project is also responsible for creating a connection with the server, asking for a file, receiving the file, and saving the file if wanted. While implementing the project, UDP mechanism must be utilized as the transport layer. The implemented protocol must contain the features listed below:
•	The text file should be transferred one line at a time and each line should be numbered and stored in one UDP datagram.
•	The server must receive confirmation about the previous line before sending another line. 
•	After the confirmation of the last sent line, the server should send a last virtual line with number 0 and with 0 characters to indicate that the transfer has ended.
•	The server must only send ASCII text files not the specific characters such as new line, tab or end-of-file


2.	Functionality of The System:
The functionality of the system can be split in two: Server and client side. In this section the features of the system and the techniques used to handle the requirements are explained. For the whole system UDP is used for the transport layer with additional checking protocols created specifically for this project. The protocol created for the system is explained in the section 3. Communication Systems’ Explanation

    2.1. Server-Side Functionalities:
The server side of the project is responsible for receiving a connection from the client, receiving the number of the text file and sending the wanted text file. The server-side is implemented in such a way that it is able to communicate with multiple clients at the same time. To achieve this concurrent programming is used. The server side is required to have a list.cfg file that contains and numbers all the files that are in the local storage. Number 0, the first file, must be itself. The contents of an example list.cfg file is shown below. This file must be created and organized by the management system of the server. It can be handled with automatic and non-automatic systems. In the project, it is not required to create a management system for the organization of the cfg file, so it is not implemented. The file and its contents is created by hand. The wanted download files are also created by hand and written to the cfg file. The files can be reached from the project folder. The functionalities and their implementation is explained thoroughly below.

        2.1.1 Receiving A Connection From A Client:
The server is required to receive connections from clients. To make it applicable for multi-client usage, concurrent programming techniques are used. Instead of thread system in python, multi-processing is utilized. The main difference is, in multi-threading only one CPU core can be used. Therefore, the system doesn’t really work concurrently but it is stopping one thread and starting another thread in different time continuum. However, multi-processing system allow the program to work concurrently by using different cores in the CPU. The server works on 2 different ports. The first port is a general port that can be used by everybody to send a request to the server. The second port is used to handle other tasks such as file transfer. When the server receives a message, it calls a request handler function in a concurrent way. The request handler function creates another port in the system and starts communicating with the client over this port. The client also changes the port that it’s going to send the messages to. Every connected client has their own private port in the server, and they use it to communicate with the server. 

        2.1.1 Receiving The Selected File Number For Download: 
To connect, the client sends a package to the server. The package can be a message requesting for a file download. To make it easier to use, in the beginning of the app the client automatically sends a file transfer request for the list.cfg file. It reads the contest and shows to the user. By this, the user can choose the file he/she wants to download. In the server side of the project, it receives the request message through the general port. After the receival of the message, it creates a thread to handle the client. The thread creates a different port to communicate privately with the client. The thread searches for the file that is requested to be downloaded in the list.cfg file. If it can find the file there, it creates a file IO to read the file line by line. If the file is not found, the server sends a message to inform the user that the file is not found. To request download, the client sends a DownloadRequetPackage.

        2.1.2 Transferring the Requested File:
To transfer the file, the server uses a TextFilePackage protocol. The protocol is explained in the 3. Section of the report. In short, the server finds the file and starts reading it line by line. It sends each line to the client and then waits for an acknowledgement. Until it receives the acknowledgement, it doesn’t send another package. When it receives the acknowledgement, it starts sending the next line. When the end of the file is sent and received an acknowledgement, the server sends a message that has only 0 in it. This is used to indicate that the file transfer is finished. Every package consist of the package type, the line number, number of characters that are going to be sent and the message. Therefore, the client knows which line is sent. 

        2.1.3 In Case No Message Is Received:
After sending a text file package, if there is no message received from the client, the server sends the last sent message again. The server tries to get a connection by sending the last sent file for a certain amount of time. 

    
    2.2 Client-Side Functionalities:
    The client side of the project is responsible for interacting with the user and convert the requests into action. The client-side is responsible for communicating with the server to request a file, receiving the file and saving the file. 
    
        2.2.1 User Interface:
    The user interface of the project is a basic terminal-based UI. It asks for the number of the file you want to download. Moreover, it also asks for if you want to save the file into a local storage. 
    
        2.2.2 Requesting a File:
    The client-side uses DownloadRequestPackage to request a file from the server. If it is the first time to request a file, it sends the message to the general server port. After that, it receives the file from a different port of the server. Then it continues the communication on that port. To request the file from the server, it sends the number of the file that is retrieved from the user by UI. The package includes the package type and the file number.
    
        2.2.3 Receiving a File:
    The client-side receives the message that is described in the TextFilePackage class. When the file is received, the program shows the message in the terminal. If the user also requested the file to be downloaded, it saves the line into the file that is named by the user. If the file exists, the application overwrites the file. Therefore, be careful not to choose an already existing file. After the receival of the message, it sends back an acknowledgment message stating that it received the line. It does this by sending the line number that is received. To do this the client uses AcknowledgementPackage. After receiving the message 0 which indicates the end of file, it stops writing to the file and shows user the main menu. 
    
        2.2.3 In Case No Message Is Received:
    After sending a request package or an acknowledgement package, if there is no message received from the server, the client sends the last sent message again. The client tries to get an connection by sending the last sent file for a certain amount of time. 

3.	Communication System’s Explanation
In this section, the communication system that is used is explained. The implemented protocol that ensures that the file is not lost is reasoned and shown. All the protocol is on top of the UDP. In the created protocol which is called TFTP (Text File Transfer Protocol), there are 3 different types of message templates. They are called: Download Request Package, Acknowledgement Pacakage and Text File Package. The listed packages are implemented as classes. Every package has its own class. The classes are responsible for creating the appropriate messages, parsing the received messages and saving them as variables. All of the packages uses string based message system to communicate with the server. The variables in the same package are separated by a semi colon (;). 
3.1 Download Request Package:
This package is used to ask for a specific file to be downloaded. The class that implements the usage of this package is called DownloadRequestPackage. The package must contain the package type indicating that this is a download request package and the file number which indicates the chosen file. 

# DOWNLOAD REQUEST PACKAGE EXPLANATION --------------------------
    # [PT][FN]
        # [PT]  -> Package Type
        # [FN]  -> File Number
        # Package: [PT] ; [FN]
# DOWNLOAD REQUEST PACKAGE EXPLANATION --------------------------
3.2 Text File Package :
This package is used to send the lines in the file to the client. The class that implements the usage of this package is called TextFilePackage. The package must contain the package number, line number, number of characters inside the message and the message. The number of characters inside the message is used to check if every bit of the message is transferred without any loss. The line number is sent to inform the user which line is sent. Then the client can use this information to send an acknowledgement message. The variables are separated by semi colon (;). The protocol is string based.

# FILE PACKAGE EXPLANATION --------------------------------------
    # [PT][LN][NC][MSG]
        # [PT]  -> Package Type
        # [LN]  -> Line Number
        # [NC]  -> Number of Characters
        # [MSG] -> Message
# FILE PACKAGE EXPLANATION --------------------------------------
3.2 Acknowledgement Package :
This package is used to acknowledge the server that the specified line is received. The class that implements the usage of this package is called AcknowledgementPackage.  This package is created after the receival of the text file package. The protocol contains the package type and the line that is received. The protocol is string based and the variables are separated by semi colon (;). 

# ACKNOWLEDGEMENT PACKAGE EXPLANATION ---------------------------
    # [PT][ALN]
        # [PT]  -> Package Type
        # [ALN] -> Acknowledgement Line Number
# ACKNOWLEDGEMENT PACKAGE EXPLANATION ---------------------------


4.	Simulation On Core:

To test the written code in real life, the core emulation system was used. In the system 3 computers are used, one as a server and the others as clients. The switch is used to connect the clients to the router. The server directly connected to the router. Therefore, the clients and the servers are placed in different subnets which are controlled by the router. To upload the written code to the computers, the emulation is started and the code is copied and pasted by using nano. When all the computers have the respective code, the simulation is started. In the server side of the simulation, there are 3 files that are ready to be downloaded. One of them is list.cfg file which contains every file in the server. The others are file1.txt and file2.txt.Then the codes are started by using python command. Both of the clients connect to the server, and they ask for a file. In the start both of them automatically asks for the list.cfg file. The server handles the requests concurrently. By using multiprocessing, both of the clients receive the files concurrently. In the code, the IP addresses of the clients and the server must be changed by hand. After attending true IP addresses to the code, the simulation is ready to be used. The pictures from the working simulation can be found below.
