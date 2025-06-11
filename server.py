import threading
import socket
import time

IP_HOST='127.0.0.1'
PORT_HOST=20156
clientes={}
lock=threading.Lock()

def inputes(sockets,adres):
    username=None
    try:
        while True:
            username=sockets.recv(1024).decode('utf-8')
            prov=True
            with lock:
                if not username in clientes:
                    prov=False
            if not prov:
                break
            else:
                sockets.send('Такой логин уже занет\n Введите другой:'.encode('utf-8'))
                
            
        with lock:
            clientes[username]=sockets
        
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
                    if user in clientes:
                        clientes[user].send(f"{username} отправил вам: {inform}".encode('utf-8'))
                        sockets.send(f'Сообщение доставлено {user}'.encode('utf-8'))
                    else:
                        sockets.send(f"Пользоваиеля с таким логином {user} не существует".encode('utf-8'))
                except ValueError:
                    sockets.send("Неверный формат сообщения. Используйте:\"\\->\\Имя сообщение\"".encode('utf-8'))
            else:
                send(f'{username}:{text}',sockets) 
    except ConnectionResetError :
        if username!=None:
            with lock:
                if username in clientes:
                    del clientes[username]
            sockets.close()
            print(f"{username} отключился")
        else:
            print(f"{adres} отключился")
        

def send(text, sock):
    with lock:
        for user in clientes:
            if clientes[user]!=sock:
                try:
                    clientes[user].send(text.encode('utf-8'))
                except:
                    pass


def start_servar():
    server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.bind((IP_HOST,PORT_HOST))
    server.listen()
    print('Сервер Запущен')
    while True:
        sockets,adres=server.accept()
        threading.Thread(target=inputes,args=(sockets,adres)).start()

    
start_servar()
      
  

