# -*- coding: utf-8 -*-
import socket
import threading

def run():
    def receive():
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(('localhost', 8888))
        while True:
            data = client_socket.recv(1024)  # 指定最大接收数据量为1024字节
            print(data.decode())
    thread = threading.Thread(target=receive)
    thread.start()