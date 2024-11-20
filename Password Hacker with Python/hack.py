import argparse
import socket


parser = argparse.ArgumentParser()
parser.add_argument("hostname", type=str)
parser.add_argument("port", type=int)
parser.add_argument("password", type=str)
args = parser.parse_args()

with socket.socket() as client_socket:
    address = (args.hostname, args.port)

    client_socket.connect(address)
    client_socket.send(args.password.encode())
    print(client_socket.recv(1024).decode())
