import socket
import threading
import log
import sys

clients = []
    
def handle_client(client_socket, client_address):
    clients.append(client_socket)
    
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        for client in clients:
            if client != client_socket:
                client.send(data)
    clients.remove(client_socket)
    client_socket.close()

def create_server():
    log.info("启动服务端中...")
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(('127.0.0.1', 8888))
        server_socket.listen()

        while True:
            client_socket, client_address = server_socket.accept()
            client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
            client_thread.start()
    except KeyboardInterrupt:
        log.info("正在退出WS服务端...")
        sys.exit()
create_server()