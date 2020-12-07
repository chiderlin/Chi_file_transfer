import socket
import os
import tqdm
import threading
import py7zr
import re


SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 4096
HOST = socket.gethostbyname(socket.gethostname())
PORT = 8000
# IPv4, TCP (Default)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
# path="D:/save/"
path="/tmp/test/save/"

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
    received = client_socket.recv(BUFFER_SIZE).decode('utf-8') #iso8859-1  
    filename, filesize = received.split(SEPARATOR)
    filename = os.path.basename(filename) # remove absolute path      
    filesize = int(filesize) 

    # progress bar using tqdm
    # receive file
    progress = tqdm.tqdm(range(
        filesize), f"Receiving {filename}", unit="b", unit_scale=True, unit_divisor=1024)

    with open(path+filename, "wb") as f:
        for i in progress:
            bytes_read = client_socket.recv(BUFFER_SIZE)
            if not bytes_read:
                break
            f.write(bytes_read)
            progress.update(len(bytes_read))  # update progress bar
    if ".7z" in filename:
        save = path+filename
        unzip(save)
        os.remove(save)

    client_socket.send("File received".encode())



def unzip(filename):
    with py7zr.SevenZipFile(filename, mode='r') as z:
        z.extractall(path=path)




# client_socket.close()
# server.close()


if __name__ == "__main__":
    start()
