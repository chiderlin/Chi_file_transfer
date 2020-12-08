import socket
import tqdm
import os


SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 4096
HOST = "10.80.1.20"
# HOST = socket.gethostbyname(socket.gethostname())
def sendfile(filename, PORT):
    filesize = os.path.getsize(filename)
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(f"[+] Connecting to {HOST}:{PORT}")
    client.connect((HOST, PORT))
    print("[+] Connected.")
    client.send(f"{filename}{SEPARATOR}{filesize}".encode())
    import time
    time.sleep(1)
    # make progress bar using tqdm
    progress = tqdm.tqdm(range(
        filesize), f"Sending {filename}", unit="b", unit_scale=True, unit_divisor=1024)
    with open(filename, "rb") as f:
        for i in progress:
            bytes_read = f.read(BUFFER_SIZE)
            if not bytes_read:
                break

            client.sendall(bytes_read)
            progress.update(len(bytes_read))

    client.close()


def sendmsg(msg, PORT):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(f"[+] Connecting to {HOST}:{PORT}")
    client.connect((HOST, PORT))
    print("[+] Connected.")
    message = msg.encode()
    client.send(message)
    print(client.recv(2048).decode())
    client.close()


def port_setting(PORT, filename=None, msg=None):
    if PORT == 8000:
        sendfile(filename, PORT)
    elif PORT == 8001:
        sendmsg(msg, PORT)


def main():
    port_setting(8000, filename=r'C:/Users/chi.lin/Desktop/work2/2020-11-20_134018_Log.7z')
    # port_setting(8001, msg="test hello")


if __name__ == "__main__":
    main()
