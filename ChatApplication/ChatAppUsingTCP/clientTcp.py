import select
import socket
import threading
import time
import _thread
import sys
import logging



def server_single_client():
    print("Welcome to chat room")
    print("initialising......")
    time.sleep(1)

    s_host = socket.gethostname()
    port = 6387
    ip = socket.gethostbyname(s_host)

    sock_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock_client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print("Host: {}, IP_Address: ({})".format(s_host, ip))

    host = input(str("Enter server address: "))
    name = input("Enter your name: ")
    print("trying to connect {} on port {}".format(host, port))
    time.sleep(1)
    sock_client.connect((host, port))
    print("Connected")

    sock_client.send(name.encode())
    s_name = sock_client.recv(1024)
    s_name = s_name.decode()

    print("{} has joined chat room\n Enter e to exit chat room\n".format(s_name))
    try:
        while True:
            message = sock_client.recv(1024)
            message = message.decode()
            print("-> {} : {}".format(s_name, message))
            message = input("-> ")
            if message.lower() == 'e':
                message = "chat has been disconnected!"
                sock_client.send(message.encode())
                print("\n")
                break
            else:
                sock_client.send(message.encode("utf-8"))
    except socket.error:
        print("Error!! {}".format(socket.error))


host = socket.gethostname()
port = 1234

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

client_socket.connect((host, port))
print("\nconnected to server!!!")

print(client_socket.recv(1024).decode())
username = input("-> ")
client_socket.send(username.encode())


def listen_conn():
    message = client_socket.recv(1024)
    message = message.decode()
    if message:
        print("-> "+message)


def set_interval(func, sec):
    def func_wrapper():
        set_interval(func, sec)
        func()

    t = threading.Timer(sec, func_wrapper)
    t.start()


set_interval(listen_conn, 0.1)


def server_multiple_clients():
    while True:
        message = input("-> ")
        client_socket.send(message.encode())
        print("\nmessage sent!!")

        # if message.lower() == 'e':
        #     break


def main():
    # server_single_client()
    server_multiple_clients()


if __name__ == '__main__':
    main()
