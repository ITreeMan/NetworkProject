# import socket
# import select
#
# def mainRun():
#     host = "192.168.43.41" #ip
#     port=5000
#     server = socket.socket()
#     server.bind((host, port))
#     server.listen(3) #client numbers
#     print("waiting the connection from clients: ")
#     client,addr = server.accept()
#     print ("Connected from: " + str(addr))
#
#     while True :
#         data = client.recv(1024).decode('utf-8') #byte => string
#         if not data :
#             break
#         print ("Message From Client :" + data)
#
#         #sending data back
#         data = str(data.upper())
#         client.send(data.encode())
#         client.send(data.encode('utf-8'))
#     client.close()
#
#
# if __name__ =="__main__":
#     mainRun()


import os
import socket
from threading import Timer
import threading
import time

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverRunning = True
ip = str(socket.gethostbyname(socket.gethostname()))
port = 1234

clients = {}

s.bind((ip, port))
s.listen()
print('Server Ready...')
print('Ip Address of the Server::%s' % ip)

macT = []
def showtable(macT):
    os.system('cls')
    print("----------------------------------------------------------------------------------------------")
    print('VLAN'+'\t\t\t\t'+'Mac address'+'\t\t\t   '+'Port'+'\t\t\t'+'  Type')
    print("----------------------------------------------------------------------------------------------")
    for e in macT:
        print(e[0]+'\t\t\t'+e[1]+'\t\t\t'+e[2]+'\t\t\t'+e[3])




def delTable():

    while True:
        time.sleep(30)
        if len(macT) > 0:
            macT.remove(macT[0])
            showtable(macT)



threading.Thread(target=delTable, args=(macT)).start()

# def delrow():
#     if len(macT) != 0:
#         macT.remove(macT[0])
#
#
# time = Timer(5,delrow)
#


# def findMac (macna):
#
#     for i in macT:
#         if macna == i[0]:
#             a = [i[0],i[1],i[2],i[3]]
#             macT.remove(i)
#             macT.append(a)
#
#
#
#
#
# def timerrow():
#     global time
#     if time.isAlive():
#         time.cancel()
#     time = Timer(5,delrow)
#     time.start()


def handleClient(client, uname):
    clientConnected = True
    keys = clients.keys()
    help = 'There are four commands in Messenger\n1::ping(IP) for exampl \n ping10.51.61.123 \n2:: **checkcon for check connected ip address  \n3::**quit=>To end your session\n'

    while clientConnected:
        try:
            msg = client.recv(1024).decode('ascii')

            response = 'Number of People Online\n'
            found = False
            if '**checkcon' in msg:
                clientNo = 0
                for name in keys:
                    clientNo += 1
                    response = response + str(clientNo) + '::' + name + '\n'
                client.send(response.encode('ascii'))
            elif '**help' in msg:
                client.send(help.encode('ascii'))
            elif '**broadcast' in msg:
                msg = msg.replace('**broadcast', '')
                for k, v in clients.items():
                    v.send(msg.encode('ascii'))
            elif '**quit' in msg:
                response = 'Stopping Session and exiting...'
                client.send(response.encode('ascii'))
                clients.pop(uname)
                print(uname + ' has been logged out')
                clientConnected = False
            elif 'ping' in msg:
                for name in keys:
                    if ('ping' + name) in msg:
                        msg = msg.replace('ping' + name, '')
                        macadd = msg.replace(uname+'>>', '')
                        ipcom = msg.replace('>>'+macadd, '')
                        # print("Mac Address: " + macadd)
                        # print("IP Address: " + ipcom)
                        # print("VLAN1 "+ macadd + "0/1 "+ "Dynamic")
                        # clients.get(ipcom).send('ARP1'.encode('ascii'))
                        #
                        # clients.get(name).send('ARP2'.encode('ascii'))
                        msg = 'ARP'+','+ipcom+','+name
                        for k, v in clients.items():
                            v.send(msg.encode('ascii'))


                        found = True
                if (not found):
                    client.send('Trying to send message to invalid person.'.encode('ascii'))
            elif 'MacPort' in msg:
                # for name in keys:
                #     if ('MacPort' + name) in msg:
                        # msg = msg.replace('ping' + name, '')
                        # macadd = msg.replace(uname+'>>', '')
                        # ipcom = msg.replace('>>'+macadd, '')
                        # print("Mac Address: " + macadd)
                        # print("IP Address: " + ipcom)
                        # clients.get(name).send('ARP'.encode('ascii'))
                        if 'one' in msg:
                            msg1 = msg.replace('MacPort '+'one','')

                            macAddr = msg1.split(' ')

                            if macAddr not in macT:
                                os.system('cls')
                                macT.append(macAddr)
                            else:
                                if macAddr == macT[0]:
                                    macT.remove(macAddr)
                                    macT.append(macAddr)
                                if macAddr == macT[1]:
                                    macT.remove(macAddr)
                                    macT.append(macAddr)
                            os.system('cls')
                            showtable(macT)


                                # found = True
                # if (not found):
                #     client.send('Trying to send message to invalid person.'.encode('ascii'))




            else:
                for name in keys:
                    if ('**' + name) in msg:
                        msg = msg.replace('**' + name, '')
                        print("IP Address: " + msg)
                        clients.get(name).send(msg.encode('ascii'))
                        found = True
                if (not found):
                    client.send('Trying to send message to invalid person.'.encode('ascii'))
        except:
            clients.pop(uname)
            print(uname + ' has been logged out')
            clientConnected = False


while serverRunning:
    client, address = s.accept()
    uname = client.recv(1024).decode('ascii')
    print('%s connected to the server' % str(uname))
    client.send('Welcome to Messenger. Type **help to know all the commands'.encode('ascii'))

    if (client not in clients):
        clients[uname] = client
        threading.Thread(target=handleClient, args=(client, uname,)).start()

