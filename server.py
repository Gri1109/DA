import threading
import socket

import json
import os
import user_client
DATA_POD=os.path.join(os.path.dirname(__file__),'data_podcklechen.json')
with open(DATA_POD,"r") as dp:
    data=json.load(dp)
    IP_HOST='0.0.0.0'
    PORT_HOST=data["PORT_HOST"]
FAEL_LOG_POROL=os.path.join(os.path.dirname(__file__),'log_porol.json')
lock=threading.Lock()
clientes={}
lock_ip_port=threading.Lock()
lock_log_porol=threading.Lock()



def inputes(sockets:socket,adres):
    username=None
    try:
        while True:
            username=sockets.recv(1024).decode('utf-8')
            with lock_log_porol:
                with open(FAEL_LOG_POROL,'r') as log:
                    spisok_log=json.load(log)
            if username in spisok_log["user_log_por"]:
                sockets.send('Хорошо такой пользователь есть теперь введите пороль'.encode('utf-8'))
                while True:
                    porol=sockets.recv(1024).decode('utf-8')
                    if spisok_log["user_log_por"][username]==porol:
                        break
                    else:
                        sockets.send('Неверный проль'.encode('utf-8'))
                break
            else:
                sockets.send('Такого логина нет\n Попробуете еще раз '.encode('utf-8'))
        
        
        
        with lock:
            clientes[username]=user_client.User(adres[1],sockets,username,porol)
        sockets.send(f'Вы вошли как {username}'.encode('utf-8'))
        print(f'{username} подключился с {adres}')

        while True:
            data=sockets.recv(1024)
            if not data:
                break
            text:str=data.decode()

            if text.startswith('\\->\\'):
                try:
                    user,inform=text[4:].split(' ',1)
                    with lock:
                        if user in clientes:
                            clientes[user].soc.send(f"{username} отправил вам: {inform}".encode('utf-8'))
                            sockets.send(f'Сообщение доставлено {user}'.encode('utf-8'))
                        else:
                            sockets.send(f"Пользоваиеля с таким логином {user} не существует".encode('utf-8'))
                except ValueError:
                    sockets.send("Неверный формат сообщения. Используйте:\"\\->\\Имя сообщение\"".encode('utf-8'))
            elif text.startswith('->'):
                sockets.send('Пожалуйста не используется \"->\" в начале строки если вы хотите отправить сообщению конкретному пользователь то используте такой формат:\"\\->\\Имя сообщение\"'.encode('utf-8'))
            else:
                send(f'{username}:{text}',sockets) 
    except ConnectionResetError :
        if username!=None:
            del clientes[username]
            print(f"{username} отключился")
        else:
            print(f"{adres} отключился")
        

def send(text, sock):
    with lock:
        for user in clientes:
            if clientes[user].soc!=sock:
                try:
                    clientes[user].soc.send(text.encode('utf-8'))
                except:
                    pass


def start_servar():
    server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.bind((IP_HOST,PORT_HOST))
    server.listen()
    print('\033cСервер Запущен')
    while True:
        sockets,adres=server.accept()
        threading.Thread(target=inputes,args=(sockets,adres)).start()

    
start_servar()
      
  

