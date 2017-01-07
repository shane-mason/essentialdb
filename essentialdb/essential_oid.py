
import threading
import os
import struct
import hashlib
import binascii
import time
import socket

def _gen_machine_part():
    machine_hash = hashlib.md5()
    machine_hash.update(socket.gethostname().encode())
    machine_part = machine_hash.digest()[0:3]
    return machine_part

class EssentialOID:
    """
    Inspired by the Python BSON Mongo driver implementation here:
    https://github.com/mongodb/mongo-python-driver/blob/master/bson/objectid.py
    But really just deals in generating strings
    """

    #we start at zero for our incrementer (instead of random)
    _incrementer = 0
    _incrementer_lock = threading.Lock()
    _machine_part = _gen_machine_part()
    _process_part = struct.pack(">H", os.getpid() % 0xFFFF)


    @staticmethod
    def generate_next_id():
        oids = []

        oid = struct.pack(">i", int(time.time()))
        oid += EssentialOID._machine_part
        oid += EssentialOID._process_part
        with EssentialOID._incrementer_lock:
            oid += struct.pack(">i", EssentialOID._incrementer)[1:4]
            EssentialOID._incrementer = (EssentialOID._incrementer + 1) % 0xFFFFFF

        return binascii.hexlify(oid).decode()

