from socket import *
import pickle


class Packet:
    pass


IP = '127.0.0.1'
PORT = 12345

receiver_socket = None


def send_ACK():
    pass


def receiving_packets():
    last_ack = None
    buffer = {}
    while True:
        data, addr = receiver_socket.recvfrom(4096)
        packet = pickle.loads(data)
        if packet.seq_number > last_ack:
            if packet.seq_number not in buffer:
                buffer[packet.seq_number] = packet
        elif packet.seq_number < last_ack:
            send_ACK()
        else:
            if not buffer:
                last_ack += len(packet.payload)
                send_ACK()
            else:
                buffer[packet.seq_number] = packet


if __name__ == '__main__':
    receiver_socket = socket(AF_INET, SOCK_DGRAM)
    receiver_socket.bind((IP, PORT))
    receiving_packets()
