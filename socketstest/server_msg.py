import socket
import os
import tqdm
import threading


BUFFER_SIZE = 64
HOST = socket.gethostbyname(socket.gethostname())
PORT = 8001

# IPv4, TCP (Default)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))


def start():
    server.listen()
    print(f"[*] Listening as {HOST}:{PORT}")
    while True:
        client_socket, addr = server.accept()
        thread = threading.Thread(
            target=handle_msg, args=(client_socket, addr))
        thread.start()
        print(f"[*] Active connections {threading.activeCount()}")


def handle_msg(client_socket, addr):
    print(f"[+] {addr} is connected.")
    msg = client_socket.recv(BUFFER_SIZE).decode()
    print(f"[{addr}] {msg}")
    client_socket.send("Msg received".encode())


if __name__ == "__main__":
    start()
