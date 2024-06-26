import os
import shutil
import ctypes
from multiprocessing import Process

from agent import run 
from config import NODES

#Message = cython.struct(
#        sender=cython.int,
#        receiver=cython.int,
#        msg=cython.char)

if __name__ == "__main__":
    network = "/tmp/pbft"
    shutil.rmtree(network, ignore_errors=True)
    os.mkdir(network)
    #run(0, network)
    for i in range(NODES):
        p = Process(target=run, args=(i, network))
        p.start()

