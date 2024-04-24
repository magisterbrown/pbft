import socket
import ctypes
import struct

from msg import type_ids, id_to_type, ClientRequest, PrePrepare, PreSend, Prepare, Commit, ClientResponse
from config import NODES, F
from statemachine import FSM

def sende(trg: int, msg):

    sendsock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    sendsock.connect(f"/tmp/pbft/{trg}.sock")
    sendsock.sendall(type_ids[type(msg)].to_bytes(4))
    sendsock.sendall(bytes(msg))
    sendsock.close()

def run(idx: int, network: str):
    view=0
    seqn=0
    presend_hist = list()
    prep_hist = list()
    commit_hist = list()

    server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    server.bind(f"{network}/{idx}.sock")
    server.listen(NODES)
    machine = FSM("./fsm.json")

    pending_msg=list()
    out_of_context=list() # Future consensus to be executed
    try:
        while True:
            connection, client_address = server.accept()

            typer = id_to_type[int.from_bytes(connection.recv(4))]
            req = typer()
            connection.recv_into(req)
            match req:
                case ClientRequest():
                    if view%NODES == 0:
                        prepre = PrePrepare(view=view, seq=seqn)
                        seqn+=1

                        pre_send = PreSend(pre=prepre, req=req)
                        presend_hist.append(pre_send)

                        msg = Prepare(replica_id=idx, pre=prepre) 
                        prep_hist.append(msg)

                        for i in range(NODES):
                            if i != idx:
                                sende(i, pre_send)
                                sende(i, msg)
                               

                case PreSend():
                    prep = req.pre
                    new_prep = all([x.pre != prep for x in presend_hist])
                    #TODO: check seq between h and H
                    if req.pre.view == view and new_prep:
                        presend_hist.append(req)
                        msg = Prepare(replica_id=idx, pre=prep) 
                        prep_hist.append(msg)
                        for i in range(NODES):
                            if i != idx:
                                sende(i, msg)
                    else:
                        raise Exception("Broken presend")
                case Prepare():
                    prep_hist.append(req)
                    prep = req.pre
                    preprepare_exists = any([x.pre == prep for x in presend_hist])
                    prepare_amount = sum([x.pre == prep for x in prep_hist])
                    if preprepare_exists and prepare_amount==(2*F+1):
                        print("Prepared")
                        commit = Commit(pre=prep, replica_id=idx)
                        commit_hist.append(commit)
                        for i in range(NODES):
                            if i != idx:
                                sende(i, commit)

                case Commit():
                    commit_hist.append(req)
                    commitsn=sum([x.pre == req.pre for x in commit_hist])
                    if commitsn == (2*F+1):
                        for presend in presend_hist: 
                            if presend.pre == req.pre:
                                news = machine.next(presend.req.op.decode())
                                resp = ClientResponse(num=presend.pre.seq, req=presend.req, res=news.encode())
                                sendsock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
                                sendsock.connect(f"/tmp/pbft/listener.sock")
                                sendsock.sendall(bytes(resp))
                                sendsock.close()


                                break
                case _:
                    raise Exception("Wrong msg type")

    except KeyboardInterrupt:
        print(f"{idx} exited")

