from socket import *
from threading import Thread
from datetime import *
import sys
from time import sleep

TIME = '%Y-%m-%d %H:%M:%S'
id_list = []
socket_list = []

# 创建监听套接字
HOST = '0.0.0.0'
PORT = 8888
ADDR = (HOST,PORT)
s = socket()  # 创建TCP套接字
s.bind(ADDR)
s.listen(3)


def recv(c, id):
    try:
        return c.recv(2048).decode()  # 获取此套接字（用户）发送的消息
    except:
        curtime = datetime.now().strftime(TIME)
        socket_list.remove(c)
        id_list.remove(id)
        for s in socket_list:
            s.send(curtime.encode())
            s.send(('系统消息： ' + id + ' 离开了聊天室!').encode())
            sleep(1)
        for i in range(len(socket_list)):
            for j in range(len(id_list)):
                a = 'id ' + id_list[j]
                socket_list[i].send(a.encode())
                sleep(1)
        c.close()


def send(c):
    socket_list.append(c)
    id = c.recv(1024).decode()
    id_list.append(id)
    curtime = datetime.now().strftime(TIME)
    for s in socket_list:
        s.send(curtime.encode())
        sleep(1)
        s.send(('系统消息： ' + id + ' 进入了聊天室！').encode())
        sleep(1)
    for i in range(len(socket_list) - 1):
        a = 'id ' + id
        socket_list[i].send(a.encode())
        sleep(1)
    for i in id_list:
        a = 'id ' + i
        c.send(a.encode())
        sleep(1)

    try:
        while True:
            data = recv(c,id)  # 获取用户发送的消息
            if not data:
                break
            else:
                curtime = datetime.now().strftime(TIME)
                for s in socket_list:  # 其他套接字通知
                    s.send(curtime.encode())
                    s.send((id + ':' + data).encode())
    except:
        print('Error!')


while True:
    try:
        c, addr = s.accept()
    except Exception as e:
        print(e)
        sys.exit('服务器退出')

    t = Thread(target=send,args=(c,))
    t.setDaemon(True)
    t.start()
