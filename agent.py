import socket
import ctypes

from msg import Message

def run(idx: int, network: str):
    server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    server.bind(f"{network}/{idx}.sock")
    server.listen(1)
    try:
        while True:
            connection, client_address = server.accept()
            req = Message()
            connection.recv_into(req)
            print(f"from {req.from_id}")
            print(f"to {req.to_id}")
            print(f"msg {req.msg}")
            #print(client_address)
            connection.close()
    except KeyboardInterrupt:
        print(f"{idx} exited")

