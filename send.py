import socket
from msg import Message

if __name__ == "__main__":
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    sock.connect("/tmp/pbft/0.sock")
    data = Message(23,34,b"T")
    print(data.from_id)
    sock.sendall(bytes(data))
    sock.close()
