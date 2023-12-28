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


def receiving_packets():
    global state
    global packet
    while True:

        if state == 0:
            data, addr = receiver_socket.recvfrom(4096)
            packet = pickle.loads(data)
            if packet.seq_number == 1:
                response = Packet(seq_number=0, last_ack=1, payload='')
                receiver_socket.sendto(pickle.dumps(response), addr)
            else:
                sender_socket.sendto(bytes(packet.payload, encoding='utf8'), (DEST_IP, DEST_PORT))
                response = Packet(seq_number=0, last_ack=0, payload='')
                receiver_socket.sendto(pickle.dumps(response), addr)
                state = 1
        elif state == 1:
            data, addr = receiver_socket.recvfrom(4096)
            packet = pickle.loads(data)
            if packet.seq_number == 0:
                response = Packet(seq_number=0, last_ack=0, payload='')
                receiver_socket.sendto(pickle.dumps(response), addr)
            else:
                sender_socket.sendto(bytes(packet.payload, encoding='utf8'), (DEST_IP, DEST_PORT))
                response = Packet(seq_number=0, last_ack=1, payload='')
                receiver_socket.sendto(pickle.dumps(response), addr)
                state = 0


if __name__ == '__main__':
    receiver_socket = socket(AF_INET, SOCK_DGRAM)
    receiver_socket.bind((IP, PORT))

    sender_socket = socket(AF_INET, SOCK_DGRAM)

    receiving_packets()
