import socket
import threading

# 创建套接字
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 连接到服务端
server_address = ('127.0.0.1', 8888)
client_socket.connect(server_address)
print("已连接到服务器")

def receive_message():
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        print("收到来自服务器的消息：", data.decode())

# 创建一个新线程来处理接收消息
receive_thread = threading.Thread(target=receive_message)
receive_thread.start()

while True:
    # 发送消息到服务端
    message = input("请输入要发送的消息：")
    client_socket.send(message.encode())

    if message.lower() == 'exit':
        break

