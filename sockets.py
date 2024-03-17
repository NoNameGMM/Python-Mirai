import socket
import threading
import log
import re

clients = []  # 保存所有连接的客户端套接字

def is_positive_integer(s):
    if s.isdigit() and int(s) > 0:
        return True
    return False

def get_string_from_third_word(input_string):
    words = input_string.split()
    if len(words) >= 3:
        result = ' '.join(words[2:])
        return result
    else:
        return ""

def send(message):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 8888))
    client_socket.send(message.encode())
    
# 定义服务器端函数
def runsocket():
    def create_server():
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(('localhost', 8888))
        server_socket.listen(2)
        
        while True:
            client_socket , addr= server_socket.accept()
            clients.append(client_socket)  # 将新连接的客户端套接字保存到列表中
            data = client_socket.recv(1024)
            words = data.split()
            if not data:
                continue  # 如果接收到空数据，跳出循环避免卡住
            elif len(words) >= 2:
                first_word = words[0]
                second_word = words[1]
                if first_word == b"sendgroupmessage":
                    if is_positive_integer(second_word):
                        if len(words) >= 3:
                            third_word_onwards = b' '.join(words[2:])
                            log.info(f"向 {second_word.decode()} 发送 >> {third_word_onwards.decode()}")
                            
                            # 向除了发送客户端以外的其他客户端发送消息
                            for client in clients:
                                if client != client_socket:
                                    client.send(f"{first_word.decode()} {second_word.decode()} {third_word_onwards.decode()}".encode())
                        else:
                            log.warning("接收到的消息没有足够的单词")
                    else:
                        log.warning("第二个单词不是正整数")
                else:
                    log.warning("第一个单词不是'sendmessage'")
            else:
                log.warning("awa")
    
    # 创建并启动服务器线程
    server_thread = threading.Thread(target=create_server)
    server_thread.start()

