import socket
import sys
import _thread
import time
import select
connection = []


def single_client():
    print("Welcome to chat room")
    print("initialising......")
    time.sleep(1)

    host = ''
    port = 6387
    ip = socket.gethostbyname(host)

    sock1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock1.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock1.bind((host, port))
    print("Host: {}, IP_Address: ({})".format(host, ip))
    name = input("Enter your name: ")

    sock1.listen(1)
    print("\nwaiting for incoming connections........\n")
    con, address = sock1.accept()
    print("server {} connected on Port: {}".format(address[0], address[1]))

    s_name = con.recv(1024)
    s_name = s_name.decode()
    print("{} has connected to chat room\n Enter e to exit chat room\n".format(s_name))
    con.send(name.encode())

    try:
        while True:
            message = input("-> ")
            # if message.lower() == 'e':
            #     message = "chat disconnected!!"
            #     con.send(message.encode())
            #     print("\n")
            #     break
            con.send(message.encode())
            message = con.recv(1024)
            message = message.decode()
            # print("{} : {}".format(s_name, message))
    except socket.error:
        print("Error! {}".format(socket.error))


def multiple_clients(conn):
    conn.send("\nwelcome to server".encode())
    conn.send("\nenter your name: ".encode())
    s_name = conn.recv(1024)
    s_name = s_name.decode()

    broadcast(conn, "\n-----"+s_name+" joined chat-----")

    print("\n{} is connected".format(s_name))

    while True:
        received_msg = conn.recv(1024)
        received_msg = received_msg.decode()
        print(received_msg)
        if received_msg:
            received_msg = s_name+'->'+received_msg
        broadcast(conn, received_msg)


def broadcast(conn, msg):
    for client_con in connection:
        if client_con == conn:
            pass
        else:
            client_con.send(msg.encode())


def main():
    # single_client()
    global connection
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    host = socket.gethostname()
    port = 1234

    server_socket.bind((host, port))

    server_socket.listen(10)
    print("waiting for connections!!!!")
    while True:
        conn, addr = server_socket.accept()
        connection.append(conn)
        print(connection)
        _thread.start_new_thread(multiple_clients, (conn, ))


if __name__ == '__main__':
    main()
