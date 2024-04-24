import socket
import random 
import struct
import os
import signal
import time

from msg import ClientRequest, ClientResponse, type_ids 
from config import NODES, F

view=1
if __name__ == "__main__":
    responses = dict()
    req = ClientRequest(uuid=random.randint(0, 10000), op=b"B")
    responses[req.uuid] = list()
 
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    sock.connect(f"/tmp/pbft/{view%NODES}.sock")

    sock.sendall(type_ids[ClientRequest].to_bytes(4))
    sock.sendall(bytes(req))
    sock.close()

    respsock = "/tmp/pbft/listener.sock"
    os.remove(respsock) if os.path.exists(respsock) else None
    server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    server.bind(respsock)
    server.listen(NODES)

    for k in range(2*F+1):
        connection, client_address = server.accept()
        resp = ClientResponse()
        connection.recv_into(resp)
        connection.close()
        responses[resp.req.uuid].append(resp.res)

    print(responses)

