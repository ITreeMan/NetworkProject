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


import socket
import threading

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverRunning = True
ip = str(socket.gethostbyname(socket.gethostname()))
port = 1234

clients = {}
list_of_connected = []

s.bind((ip, port))
s.listen()
print('Server Ready...')
print('Ip Address of the Server::%s' % ip)


def handleClient(client, uname):
    clientConnected = True
    keys = clients.keys()

    help = 'There are four commands in Messenger\n1::**chatlist=>gives you the list of the people currently online\n2::**quit=>To end your session\n3::**broadcast=>To broadcast your message to each and every person currently present online\n4::Add the name of the person at the end of your message preceded by ** to send it to particular person'

    while clientConnected:
        try:
            msg = client.recv(1024).decode('ascii')
            #response = 'Show MAC address table\n'
            found = False
            if 'show mac' in msg:
                e = list_of_connected[0]
                print("ip: " + e.get('ip') + " mac: " + e.get('mac') + " port: " + e.get('port'))

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
                        print('msg '+msg)
                        myip=msg.replace(','+'ping'+name,'')

                        print('iptarget= '+myip+' myip =  '+myip)
                if (not found):
                    client.send('Trying to send message to invalid person.'.encode('ascii'))
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
    unameall=uname
    ipadd,macadd,portadd = uname.split(",")
    print('%s connected to the server' % str(ipadd))
    client.send('Welcome to Messenger. Type **help to know all the commands'.encode('ascii'))

    if (client not in clients):
        clients[ipadd] = client
        list_of_connected.append({
            'ip': ipadd,
            'mac': macadd,
            'port': portadd
        })
        threading.Thread(target=handleClient, args=(client, (ipadd,macadd,portadd),)).start()
        print(str(address))


