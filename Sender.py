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

state = 0
start_time = None
stop_thread = False
clock = None
packet = None


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


def start_timer():
    global start_time
    global stop_thread
    global clock
    start_time = time.time()
    stop_thread = False
    clock = threading.Thread(target=timer)
    clock.start()


def stop_timer():
    global stop_thread
    stop_thread = True


def add_headers_and_send_packet(data, seq_number):
    global packet
    packet = Packet(seq_number, 0, data.decode())
    sender_socket.sendto(pickle.dumps(packet), (DEST_IP, DEST_PORT))


def stop_state_handler(seq_number, next_state):
    global state
    data, addr = receiver_socket.recvfrom(4096)
    add_headers_and_send_packet(data, seq_number)
    start_timer()
    state = next_state


def wait_state_handler(needed_ack, next_state):
    global state
    data, addr = sender_socket.recvfrom(4096)
    response = pickle.loads(data)
    if response.last_ack == needed_ack:
        stop_timer()
        state = next_state


def sending_packets():
    global state
    while True:
        if state == 0:
            stop_state_handler(seq_number=0, next_state=1)

        elif state == 1:
            wait_state_handler(needed_ack=0, next_state=2)

        elif state == 2:
            stop_state_handler(seq_number=1, next_state=3)
        elif state == 3:
            wait_state_handler(needed_ack=1, next_state=0)


if __name__ == '__main__':
    sender_socket = socket(AF_INET, SOCK_DGRAM)
    receiver_socket = socket(AF_INET, SOCK_DGRAM)
    receiver_socket.bind((RECEIVER_IP, RECEIVER_PORT))
    sending_packets()
