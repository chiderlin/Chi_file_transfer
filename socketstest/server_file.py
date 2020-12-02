import socket
import os
import tqdm
import threading

SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 4096
HOST = socket.gethostbyname(socket.gethostname())
PORT = 8000
# IPv4, TCP (Default)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))


def start():
    server.listen()
    print(f"[*] Listening as {HOST}:{PORT}")
    while True:
        client_socket, addr = server.accept()
        thread = threading.Thread(
            target=handle_file, args=(client_socket, addr))
        thread.start()
        print(f"[*] Active connections {threading.activeCount()}")


def handle_file(client_socket, addr):
    print(f"[+] {addr} is connected.")
    received = client_socket.recv(BUFFER_SIZE).decode()
    filename, filesize = received.split(SEPARATOR)
    filename = os.path.basename(filename) # remove absolute path      
    filesize = int(filesize)

    # progress bar using tqdm
    # receive file
    progress = tqdm.tqdm(range(
        filesize), f"Receiving {filename}", unit="b", unit_scale=True, unit_divisor=1024)
    with open(r"D:/save//"+filename, "wb") as f:
    # with open(r"/tmp/test/save//"+filename, "wb") as f:
        for i in progress:
            bytes_read = client_socket.recv(BUFFER_SIZE)
            if not bytes_read:
                break
            f.write(bytes_read)
            progress.update(len(bytes_read))  # update progress bar
    client_socket.send("File received".encode())

# client_socket.close()
# server.close()


if __name__ == "__main__":
    start()
