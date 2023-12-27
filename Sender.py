from socket import *
if __name__ == '__main__':
    sender_socket = socket(AF_INET, SOCK_DGRAM)
    sender_socket.bind(('',8585))
    sender_socket.sendto(b'Salam koon', ('',12345))

