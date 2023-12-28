from socket import *
import pickle


class Packet:
    def __init__(self, seq_number, last_ack, payload):
        self.seq_number = seq_number
        self.last_ack = last_ack
        self.payload = payload


IP = '127.0.0.1'
PORT = 54321

DEST_IP = '127.0.0.1'
DEST_PORT = 5080

receiver_socket = None
sender_socket = None

state = 0

packet = None


def creating_response(ack_number):
    return Packet(seq_number=0, last_ack=ack_number, payload='')


def sending_response(ack_number, sender_address):
    response = creating_response(ack_number)
    response_packet = pickle.dumps(response)
    receiver_socket.sendto(response_packet, sender_address)


def transfer_payload():
    global packet
    transfer_packet = bytes(packet.payload, encoding='utf8')
    transfer_address = (DEST_IP, DEST_PORT)
    sender_socket.sendto(transfer_packet, transfer_address)


def state_1_handler(data, addr):
    global packet
    global state
    packet = pickle.loads(data)
    if packet.seq_number == 0:
        sending_response(0, addr)
    else:
        transfer_payload()
        sending_response(1, addr)
        state = 0


def state_0_handler(data, addr):
    global state
    global packet
    packet = pickle.loads(data)
    if packet.seq_number == 1:
        sending_response(1, addr)
    else:
        transfer_payload()
        sending_response(0, addr)
        state = 1


def receiving_packets():
    global state
    while True:
        data, addr = receiver_socket.recvfrom(4096)
        if state == 0:
            state_0_handler(data, addr)
        elif state == 1:
            state_1_handler(data, addr)


if __name__ == '__main__':
    receiver_socket = socket(AF_INET, SOCK_DGRAM)
    receiver_socket.bind((IP, PORT))

    sender_socket = socket(AF_INET, SOCK_DGRAM)

    receiving_packets()
