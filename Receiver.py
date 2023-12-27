from socket import *
import pickle


class Packet:
    def __init__(self, seq_number, last_ack, payload):
        self.seq_number = seq_number
        self.last_ack = last_ack
        self.payload = payload


IP = '127.0.0.1'
PORT = 12345

receiver_socket = None


def send_ACK(last_ack, addr):
    packet = Packet(seq_number=1, last_ack=last_ack, payload='')
    receiver_socket.sendto(pickle.dumps(packet), addr)


def ack_until_now(buffer):
    sequence = sorted(buffer.keys())
    for index, seq_number in enumerate(sequence[:-1]):
        print(f'sequence number: {seq_number}, payload: {buffer[seq_number].payload}\n')
        if sequence[index] + len(buffer[seq_number].payload) == sequence[index + 1]:
            buffer.pop(seq_number)
        else:
            last_ack = sequence[index] + len(buffer[seq_number].payload)
            buffer.pop(seq_number)
            return buffer, last_ack


def receiving_packets():
    last_ack = 0
    buffer = {}
    while True:
        data, addr = receiver_socket.recvfrom(4096)
        packet = pickle.loads(data)
        if packet.seq_number > last_ack:
            if packet.seq_number not in buffer:
                buffer[packet.seq_number] = packet
            send_ACK(last_ack, addr)
        elif packet.seq_number < last_ack:
            send_ACK(last_ack, addr)
        else:
            if not buffer:
                last_ack += len(packet.payload)
                send_ACK(last_ack, addr)
            else:
                if packet.seq_number not in buffer:
                    buffer[packet.seq_number] = packet
                buffer, last_ack = ack_until_now(buffer)
                send_ACK(last_ack, addr)


if __name__ == '__main__':
    receiver_socket = socket(AF_INET, SOCK_DGRAM)
    receiver_socket.bind((IP, PORT))
    receiving_packets()
