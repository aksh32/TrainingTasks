import socket

HOST = socket.gethostname()
PORT = 50007

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sc1:
    try:
        while True:
            message = input("-> ")
            sc1.sendto(message.encode(), (HOST, PORT))
            data, address = sc1.recvfrom(1024)
            newData = data.decode()
            print("Received from server: {}".format(newData))
            if newData.lower() == 'exit':
                print("Thanks for chatting!!!!")
                break

    except socket.error:
        print("Error! {}".format(socket.error))
        exit()
