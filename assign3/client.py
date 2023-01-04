import json
import random
from socket import socket, AF_INET, SOCK_STREAM
import sys
import ast

from MerkleHellman import create_public_key, generate_private_key, decrypt_mh, encrypt_mh
from cipher import Cipher
from server import HOST_NAME, KEY_SERVER_PORT, MESSAGE_SIZE


def initialize_connection(port):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.bind((HOST_NAME, port))
    print('Client listening on port {} for connection'.format(port))
    sock.listen(1)
    while True:
        connection, _ = sock.accept()
        try:
            connection.sendall(json.dumps({
                'status': 'init',
            }).encode())
            data = json.loads(connection.recv(MESSAGE_SIZE).decode())
            # print('Received data: {}'.format(data))
            if 'status' in data and data['status'] == 'connected':
                return connection
        except Exception:
            print('Exception while connecting. Waiting for another connection')


def connect(port):
    sock = socket(AF_INET, SOCK_STREAM)
    print('Client connecting to port {}'.format(port))
    sock.connect((HOST_NAME, port))

    try:
        data = json.loads(sock.recv(MESSAGE_SIZE).decode())
        # print('Received data: {}'.format(data))
        if 'status' in data and data['status'] == 'init':
            sock.sendall(json.dumps({'status': 'connected'}).encode())
            return sock
        print('Could not connect')
        exit()
    except Exception:
        print('Could not connect')
        exit()


def register_pub_key(connection, id, key):
    connection.sendall(
        json.dumps({
            'method': 'POST',
            'id': id,
            'key': key
        }).encode()
    )
    ans = json.loads(connection.recv(MESSAGE_SIZE).decode())
    return ans['success']


def get_pub_key(connection, id):
    connection.sendall(
        json.dumps({
            'method': 'GET',
            'id': id
        }).encode()
    )
    ans = json.loads(connection.recv(MESSAGE_SIZE).decode())
    return ans['key']


def disconnect_from_key_server(connection, id):
    connection.sendall(
        json.dumps({
            'method': 'CLOSE',
            'id': id
        }).encode()
    )
    connection.close()


def send_mh_encr(connection, message, public_key):
    connection.sendall(json.dumps(encrypt_mh(
        message.encode(), public_key)).encode())


def recv_mh_encr(connection, private_key):
    return decrypt_mh(json.loads(connection.recv(MESSAGE_SIZE).decode()), private_key).decode()


def send_sol_encr(connection, cipher):
    plain_text = input('Enter your message:\n')
    if plain_text == '':
        print('Leaving')
        connection.sendall(json.dumps({'status': 'exit'}).encode())
        connection.close()
        exit()
    connection.sendall(
        json.dumps({
            'cipher_text': list(cipher.encrypt(bytes(plain_text, 'ascii')))
        }).encode()
    )
    return len(plain_text)


def recv_sol_encr(connection, cipher):
    data = json.loads(connection.recv(MESSAGE_SIZE).decode())
    if 'status' in data and data['status'] == 'exit':
        print('Peer left the connection')
        connection.close()
        exit()
    if 'cipher_text' not in data:
        return 'Invalid message received.'
    cipher_text = data['cipher_text']
    return cipher.decrypt(bytes(cipher_text)).decode()


def main():
    if len(sys.argv) <= 2:
        print('Missing argument.')
        print('Usage: {} {{id}} {{1|2}}'.format(sys.argv[0]))
        exit()
    if sys.argv[2] in ['1', 'first']:
        first_sender = True
    elif sys.argv[2] in ['2', 'second']:
        first_sender = False
    else:
        print('Incorrect argument.')
        print('Usage: {} {{id}} {{1|2}}'.format(sys.argv[0]))
        exit()
    id = int(sys.argv[1])

    # register to key server with generated public key
    private_key = generate_private_key()
    public_key = create_public_key(private_key)
    print('private and public keys generated')
    key_server_socket = connect(KEY_SERVER_PORT)
    print('connected to key server')
    while not register_pub_key(key_server_socket, id, public_key):
        pass
    print('public key sent to key server')

    # solitaire key init
    solitaire_key = random.sample([*range(1, 55)], 54)

    if first_sender:
        peer_id = int(input('id of peer = '))
        peer_socket = connect(peer_id)

        # get the public key of peer from key server
        peer_public_key = get_pub_key(key_server_socket, peer_id)
        disconnect_from_key_server(key_server_socket, id)
        print('public key of peer received from key server')

        # say hello to peer
        send_mh_encr(peer_socket, str(id), peer_public_key)
        if peer_id != int(recv_mh_encr(peer_socket, private_key)):
            print("Error: received id does not matches with known id.")
        print('connected to peer with id {}'.format(peer_id))

        print('half solitaire key generated')
        solitaire_half_key = solitaire_key[:len(solitaire_key)//2]
        random.shuffle(solitaire_half_key)
    else:
        # get the id of peer from hello message
        peer_socket = initialize_connection(id)
        peer_id = int(recv_mh_encr(peer_socket, private_key))
        print('peer with id {} connected'.format(peer_id))

        # get the public key of peer from key server
        peer_public_key = get_pub_key(key_server_socket, peer_id)
        disconnect_from_key_server(key_server_socket, id)
        print('public key of peer received from key server')

        # respond to hello message
        send_mh_encr(peer_socket, str(id), peer_public_key)

        print('half solitaire key generated')
        solitaire_half_key = solitaire_key[len(solitaire_key)//2:]
        random.shuffle(solitaire_half_key)

    # SOLITAIRE
    send_mh_encr(peer_socket, str(solitaire_half_key), peer_public_key)
    solitaire_half_key2 = ast.literal_eval(
        recv_mh_encr(peer_socket, private_key))
    print('half solitaire key received')
    if solitaire_half_key[0] < solitaire_half_key2[0]:
        solitaire_key = solitaire_half_key + solitaire_half_key2
    else:
        solitaire_key = solitaire_half_key2 + solitaire_half_key
    print(solitaire_key)
    print(len(solitaire_key))
    cipher = Cipher(solitaire_key)
    print('cipher initalized')

    # start communication
    if first_sender:
        send_sol_encr(peer_socket, cipher)

    while True:
        msg = recv_sol_encr(peer_socket, cipher)
        print('Peer messaged you: ')
        print(msg)
        send_sol_encr(peer_socket, cipher)


if __name__ == '__main__':
    main()
