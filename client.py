import threading
import socket
import os
import json
DATA_POD=os.path.join(os.path.dirname(__file__),'data_podcklechen.json')
with open(DATA_POD,"r") as dp:
    data=json.load(dp)
    IP_HOST='158.160.140.195'
    PORT_HOST=data["PORT_HOST"]


def priem(socketes):
    while True:
        try:
            data=socketes.recv(1024)
            if not data:
                break 
        except:
            break
        print(data.decode('utf-8'))

def otpravka(socketes):
    while True:
        text=input()
        socketes.send(text.encode('utf-8'))
    
def start_client():
    client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client.connect((IP_HOST,PORT_HOST))
    
    username=input('Введите ваш логин: ')
    client.send(username.encode('utf-8'))
    
    threading.Thread(target=priem,args=(client,)).start()
    otpravka(client)

    

start_client()


    
      