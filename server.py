import socket
import threading

clients = []

def handle_client(client_socket, client_address):
    try:
        clients.append(client_socket)
    
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
        
            # 将消息发送给其他客户端
            for client in clients:
                if client != client_socket:
                    client.send(data)
    
        clients.remove(client_socket)
        client_socket.close()
    except ConnectionResetError as e:
        print("一个客户端断开连接,请检查或重启机器人")

# 创建套接字
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('127.0.0.1', 8888))
server_socket.listen()

print("正在启动")

while True:
    client_socket, client_address = server_socket.accept()
    
    # 创建新线程处理客户端连接
    client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
    client_thread.start()
