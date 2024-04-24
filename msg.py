from ctypes import *

#class Message(Structure):
#    _fields_ = [("uuid", c_int),
#                ("to_id", c_int),
#                ("ordered", c_bool),
#                ("mtype", c_char * 4)]
#


class ClientRequest(Structure):
    _fields_ = [("uuid", c_int),
                ("op", c_char)]

class PrePrepare(Structure):
    _fields_ = [("view", c_int),
                ("seq", c_int)]
                #Maybe digest
    def __eq__(self, other):
        return self.view == other.view and self.seq == other.seq

class PreSend(Structure):
    _fields_ = [("pre", PrePrepare),
                ("req", ClientRequest)]

class Prepare(Structure):
    _fields_ = [("replica_id", c_int),
                ("pre", PrePrepare)]

class Commit(Structure):
    _fields_ = [("replica_id", c_int),
                ("pre", PrePrepare)]


#class ReqestSize(c_int):
#    CLIENT = 1
#    PRE_PRE = 2
#    PREPARE = 3
#    COMMIT = 4
types = (ClientRequest, PreSend, Prepare, Commit)

type_ids = dict()
id_to_type = dict()
for k,v in enumerate(types):
    type_ids[v] = k
    id_to_type[k] = v

#request_types = {
#            ReqestSize.CLIENT: ClientRequest,
#            ReqestSize.PRE_PRE: PreSend,
#            ReqestSize.PREPARE: Prepare,
#            ReqestSize.COMMIT: Commit
#        }
#print(request_types)

class ClientResponse(Structure):
    _fields_ = [("num", c_int),
                ("req", ClientRequest),
                ("res", c_char*3)]

