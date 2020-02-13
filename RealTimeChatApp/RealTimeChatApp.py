import ast
import datetime
import socket
import time
import sys
import traceback
import threading
import _thread
import redis

shutdown = False
# register a user
hostname = socket.gethostname()
port = 8888
redis_client = redis.Redis(charset='utf-8', decode_responses=True)
soc_conn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
soc_conn.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
soc_conn.bind((hostname, port))
user_data_list = 'user_info'
hist_list_name = 'chat_history'
chat_hist = {}
previous_msg = ''
global ip_address
global reg_user_name


def chat_app():
    try:
        ans = 'y'
        global ip_address
        global reg_user_name
        user_reg_data = []
        while ans.lower() == 'y':
            print('\n--------select actions--------\n1. register user\n2. view history\n3. chat')
            choice = int(input('Enter your choice: '))
            if choice == 1:
                user_name = input('Enter name: ')
                ip_add = input('Enter Ip Address: ')
                user_data = [user_name, ip_add]
                for i in range(0, redis_client.llen(user_data_list)):
                    if ip_add in redis_client.lindex(user_data_list, i):
                        print('ip address already registered with other name')
                        break
                else:
                    redis_client.lpush(user_data_list, str(user_data))
                    print('registered successfully!!!!!')
            if choice == 2:
                search_name = input('Enter a name to search: ')
                for index in range(0, redis_client.llen(hist_list_name)):
                    sent_dict = ast.literal_eval(redis_client.lindex(hist_list_name, index))
                    for key, value in sent_dict.items():
                        for ind in value:
                            if search_name == ind:
                                print(key, ' : ', value)
            if choice == 3:
                for i in range(0, redis_client.llen(user_data_list)):
                    user_reg_data.append(ast.literal_eval(redis_client.lindex(user_data_list, i)))

                print('-----select a user-----')
                for index in user_reg_data:
                    print(index[0])

                # connect to user
                u_name = input('Enter a user name: ')
                for ind in user_reg_data:
                    if u_name in ind[0]:
                        print('in for')
                        print(ind)
                        ip_address = ind[1]
                        reg_user_name = ind[0]
                        print(ip_address)
                        break
                    else:
                        print('no such user found, try to register first')

                # rec_thread = threading.Thread(target=receiving, args=(reg_user_name, soc_conn))
                # send_thread = threading.Thread(target=sending, args=(hostname, soc_conn,))
                _thread.start_new_thread(receiving,(reg_user_name, soc_conn))
                sending(hostname, soc_conn)
                # rec_thread.start()
                # send_thread.start()

                # rec_thread.join()
                # send_thread.join()
                # soc_conn.close()
            ans = input('Do you want to continue?(y/n): ')
    except KeyboardInterrupt:
        chat_app()


def receiving(name, sock):
    while True:
        try:
            data, addr = sock.recvfrom(1024)
            print('\n'+name+'> '+str(data.decode()))
            time_stamp = time.time()
            # if data:
            recv_time = datetime.datetime.fromtimestamp(time_stamp).strftime('%Y-%m-%d %H:%M:%S')
            recv_info = ['received',name, hostname, socket.gethostbyname(hostname), ip_address, recv_time, data.decode()]
            chat_hist['message'] = recv_info
            save_message(chat_hist)
            # redis_client.lpush(hist_list_name, str(chat_hist))
        except Exception as exception:
            print('receive failed!!!!!!'+str(exception))


def sending(sender, sock):
    while True:
        # try:
        message = input(sender + "> ")
        sent = sock.sendto(bytes(message, 'utf-8'), (ip_address, port))
        time_stamp = time.time()
        # if sent:
        sent_time = datetime.datetime.fromtimestamp(time_stamp).strftime('%Y-%m-%d %H:%M:%S')
        sent_info = ['sent',hostname, reg_user_name, ip_address, socket.gethostbyname(hostname), sent_time, message]
        chat_hist['message'] = sent_info
        # redis_client.lpush(hist_list_name, str(chat_hist))
        save_message(chat_hist)
        if message.lower() == '{out}':
            sock.sendto(bytes('user disconnected!!!!', 'utf-8'), (ip_address, port))
            chat_app()

        # except Exception as exception:
        #     print("send failed!!!!!!"+str(exception))


def save_message(data):
    global previous_msg
    if previous_msg == data['message'][6]:
        pass
    else:
        previous_msg = data['message'][6]
        redis_client.lpush(hist_list_name, str(data))


def main():
    chat_app()


if __name__ == '__main__':
    main()