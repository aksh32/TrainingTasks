import ast
import socket
import time
import traceback
from pprint import pprint
import threading
import redis

# tlock = threading.Lock()
shutdown = False


def receiving(name, sock):
    while not shutdown:
        try:
            while True:
                data, addr = sock.recvfrom(1024)
                print('\n'+name+'> '+str(data.decode()))
        except Exception as exception:
            print('receive failed!!!!!!'+str(exception))
            pass


def sending(sock):
    while not shutdown:
        try:
            message = input(hostname + "> ")
            while True:
                while message != 'q':
                    if message != '':
                        sock.sendto(bytes(message, 'utf-8'), (ip_address, port))
                    message = input(hostname + '> ')
                    time.sleep(0.2)
        except Exception as exception:
            print("send failed!!!!!!"+str(exception))
            pass


# register a user
hostname = socket.gethostname()
port = 8888

try:
    hash_set_name = 'user_data'
    redis_client = redis.Redis(charset='utf-8', decode_responses=True)
    choice = input("you want to register?(yes/no): ")
    if choice.lower() == 'y':
        user_name = input("Enter your name: ")
        ip_address = input("Enter IP Address: ")
        user_data = [user_name, ip_address]
        redis_client.lpush(hash_set_name, str(user_data))
        print('registered successfully!!!!!')
        # ast.literal_eval(user_data)
        # print(user_data)
    user_reg_data = {}

    for i in range(0, redis_client.llen(hash_set_name)):
        user_reg_data[i] = redis_client.lindex(hash_set_name, i)

    con_user = input("enter name: ")
    ip_address = []
    for key, value in user_reg_data.items():
        if str(value).find(con_user) != -1:
            ip_address = str(value).split(',')
            ip_address = [x.strip() for x in ip_address]
            ip_address = [x.replace('[', '') for x in ip_address]
            ip_address = [x.replace(']', '') for x in ip_address]
            ip_address = [x.replace("'", '') for x in ip_address]
            ip_address = ip_address[1]
            break

    # connect to a user
    soc_conn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    soc_conn.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    soc_conn.bind((hostname, port))
    # soc_conn.setblocking(0)

    rec_thread = threading.Thread(target=receiving, args=("RecThread", soc_conn))
    send_thread = threading.Thread(target=sending, args=(soc_conn,))
    rec_thread.start()
    send_thread.start()

    shutdown = True
    rec_thread.join()
    send_thread.join()
    soc_conn.close()

except redis.RedisError as e:
    traceback.print_exc()
    print("Error: {}".format(e))
