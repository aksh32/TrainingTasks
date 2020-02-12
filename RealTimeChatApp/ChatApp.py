import ast
import datetime
import socket
import time
import sys
import traceback
import threading
import redis

# tlock = threading.Lock()
shutdown = False

sent_data = {}
sent_list_name = 'sent_data'
recv_messages = {}
recv_list_name = 'recv_data'


def receiving(name, sock):
    while not shutdown:
        try:
            while True:
                if sock:
                    data, addr = sock.recvfrom(1024)
                    print('\n'+name+'> '+str(data.decode()))
                    time_stamp = time.time()
                    recv_time = datetime.datetime.fromtimestamp(time_stamp).strftime('%Y-%m-%d %H:%M:%S')
                    recv_info = [hostname, data.decode(), ip_address, socket.gethostbyname(hostname), recv_time]
                    recv_messages[name] = recv_info
                    redis_client.lpush(recv_list_name, str(recv_messages))
                    # print(recv_messages)
                else:
                    break

        except Exception as exception:
            print('receive failed!!!!!!'+str(exception))


def sending(sender, sock):
    while not shutdown:
        try:
            message = input(sender + "> ")
            while True:
                while message != 'q':
                    if message != '':
                        sock.sendto(bytes(message, 'utf-8'), (ip_address, port))
                        time_stamp = time.time()
                        sent_time = datetime.datetime.fromtimestamp(time_stamp).strftime('%Y-%m-%d %H:%M:%S')
                        sent_info = [con_user, message, socket.gethostbyname(hostname), ip_address, sent_time]
                        sent_data[hostname] = sent_info
                        redis_client.lpush(sent_list_name, str(sent_data))
                    message = input(sender + '> ')
                    # time.sleep(0.2)
                sock.sendto(bytes('user disconnected', 'utf-8'), (ip_address, port))
                sock.close()
                break
        except Exception as exception:
            print("send failed!!!!!!"+str(exception))


# register a user
hostname = socket.gethostname()
port = 8888

try:
    ans = 'y'
    while ans.lower() == 'y':
        user_data_list = 'user_data'
        redis_client = redis.Redis(charset='utf-8', decode_responses=True)
        print('\n--------select actions--------\n1. register user\n2. view sender data\n3. view receiver data\n4. chat')
        choice = int(input("choose option: "))
        if choice == 1:
            user_name = input("Enter your name: ")
            ip_address = input("Enter IP Address: ")
            user_data = [user_name, ip_address]
            redis_client.lpush(user_data_list, str(user_data))
            print('registered successfully!!!!!')
            # ast.literal_eval(user_data)
            # print(user_data)
        elif choice == 2:
            search_name = input('Enter a sender name to search: ')
            for index in range(0, redis_client.llen(sent_list_name)):
                sent_dict = ast.literal_eval(redis_client.lindex(sent_list_name, index))
                if search_name in sent_dict.keys():
                    print(sent_dict.values())
                else:
                    print('no such sender found!!!!!!!')
                    break
        elif choice == 3:
            name_search = input('Enter a receiver name to search: ')
            for ind in range(0, redis_client.llen(recv_list_name)):
                recv_dict = ast.literal_eval(redis_client.lindex(recv_list_name, ind))
                if name_search in recv_dict.keys():
                    print(recv_dict.values())
                else:
                    print('no such receiver found!!!!!')
                    break
        elif choice == 4:
            user_reg_data = {}

            for i in range(0, redis_client.llen(user_data_list)):
                user_reg_data[i] = redis_client.lindex(user_data_list, i)

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
                else:
                    print('no such user found, try to register first')
                    sys.exit(0)

            # connect to a user
            soc_conn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            soc_conn.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            soc_conn.bind((hostname, port))
            # soc_conn.setblocking(0)

            rec_thread = threading.Thread(target=receiving, args=(con_user, soc_conn))
            send_thread = threading.Thread(target=sending, args=('me', soc_conn,))
            rec_thread.start()
            send_thread.start()

            shutdown = True
            rec_thread.join()
            send_thread.join()
            soc_conn.close()
        ans = input("Do you want to continue?(y/n): ")

except redis.RedisError as e:
    traceback.print_exc()
    print("Error: {}".format(e))
