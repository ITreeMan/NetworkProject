# import socket
#
#
# def mainRun():
#     host = "192.168.43.98"
#     port = 5000
#     server = socket.socket()
#     server.connect((host, port))
#     data = input("input your text : ")
#
#     while data != "q":
#         server.send(data.encode("utf-8"))
#         data = server.recv(1024).decode("utf-8")
#         print("Data From Server :" + data)
#         data = input("input :")
#         server.close()
#
#
# if __name__ =="__main__":
#     mainRun()


import socket
import threading
import sys



import re
from uuid import getnode


# to get physical address:
original_mac_address = getnode()

##print("MAC Address: " + str(original_mac_address)) # this output is in raw format

#convert raw format into hex format
hex_mac_address = str(":".join(re.findall('..', '%012x' % original_mac_address)))

def getNetworkIp():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    s.connect(('<broadcast>', 0))
    return s.getsockname()[0]




ipAddress = getNetworkIp()

#print("HEX MAC Address: " + hex_mac_address)
print("Your IP Address: " + ipAddress)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = 1234
port_input = input("Enter port::")

uname = ipAddress+','+hex_mac_address+','+port_input


ip = input('Enter the IP Address of server::')

s.connect((ip, port))
s.send(uname.encode('ascii'))


clientRunning = True

def receiveMsg(sock):
    serverDown = False
    while clientRunning and (not serverDown):
        try:
            msg = sock.recv(1024).decode('ascii')
            print(msg)
        except:
            print('Server is Down. You are now Disconnected. Press enter to exit...')
            serverDown = True

threading.Thread(target = receiveMsg, args = (s,)).start()
while clientRunning:
    tempMsg = input()
    msg = ipAddress+','+tempMsg
    if '**quit' in msg:
        clientRunning = False
        s.send('**quit'.encode('ascii'))
    else:
        s.send(msg.encode('ascii'))
