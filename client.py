import socket
import threading
import log
import sys

# 创建套接字
def create_client():
    try:
        log.info("WS客户端正在启动...")
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # 连接到服务端
        server_address = ('127.0.0.1', 8888)
        client_socket.connect(server_address)
        log.info("已连接到WS服务器")

        def receive_message():
            while True:
                data = client_socket.recv(1024)
                if not data:
                    break
                log.info("收到来自服务器的消息：", data.decode())

        # 创建一个新线程来处理接收消息
        receive_thread = threading.Thread(target=receive_message)
        receive_thread.start()

        while True:
            # 发送消息到服务端
            message = input("")
            client_socket.send(message.encode())

            if message.lower() == 'exit':
                break
    except KeyboardInterrupt:
        log.info("正在退出WS客户端...")
        sys.exit()


