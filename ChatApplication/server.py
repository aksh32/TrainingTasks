import socket

HOST = socket.gethostname()
PORT = 50007

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sc1:
    sc1.bind((HOST, PORT))
    print('Connected by {}'.format(HOST))
    try:
        while True:
            data, address = sc1.recvfrom(1024)
            newdata = data.decode()
            print("from connected user: {}".format(newdata))
            message = input("-> ")
            if message.lower() == 'exit':
                sc1.sendto(message.encode(), (HOST, PORT))
            if data:
                sc1.sendto(message.encode(), address)
            if newdata.lower() == 'exit':
                break
    except socket.error:
        print("Error! {}".format(socket.error))
        exit()
