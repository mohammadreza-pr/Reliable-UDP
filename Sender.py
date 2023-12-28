import pickle
import time
import threading
from socket import *


class Packet:
    def __init__(self, seq_number, last_ack, payload):
        self.seq_number = seq_number
        self.last_ack = last_ack
        self.payload = payload


DEST_IP = '127.0.0.1'
DEST_PORT = 12345

RECEIVER_IP = '127.0.0.1'
RECEIVER_PORT = 8050

timeout_interval = 0.75


def timer():
    global sender_socket
    global start_time
    while True:
        global stop_thread
        if start_time is not None and (time.time() - start_time > timeout_interval):
            sender_socket.sendto(pickle.dumps(packet), (DEST_IP, DEST_PORT))
            start_time = time.time()
        if stop_thread:
            break


if __name__ == '__main__':
    sender_socket = socket(AF_INET, SOCK_DGRAM)

    receiver_socket = socket(AF_INET, SOCK_DGRAM)
    receiver_socket.bind((RECEIVER_IP, RECEIVER_PORT))

    state = 0

    start_time = None
    clock = None

    packet = None

    while True:
        if state == 0:
            data, addr = receiver_socket.recvfrom(4096)
            packet = Packet(0, 0, data.decode())
            sender_socket.sendto(pickle.dumps(packet), (DEST_IP, DEST_PORT))
            start_time = time.time()
            stop_thread = False
            clock = threading.Thread(target=timer)
            clock.start()
            state = 1
        elif state == 1:
            data, addr = sender_socket.recvfrom(4096)
            response = pickle.loads(data)
            if response.last_ack == 1:
                state = 1
            else:
                stop_thread = True
                state = 2
        elif state == 2:
            data, addr = receiver_socket.recvfrom(4096)
            packet = Packet(1, 0, data.decode())
            sender_socket.sendto(pickle.dumps(packet), (DEST_IP, DEST_PORT))
            start_time = time.time()
            stop_thread = False
            clock = threading.Thread(target=timer)
            clock.start()
            state = 3
        elif state == 3:
            data, addr = sender_socket.recvfrom(4096)
            response = pickle.loads(data)
            if response.last_ack == 0:
                state = 3
            else:
                stop_thread = True
                state = 0
