import hashlib
import uuid

def getHash(data=None):
    randomstr = str(uuid.uuid4())
    node = str(data) + randomstr
    iD = hashlib.md5(node.encode('utf-8')).hexdigest()
    token = str(uuid.uuid4())
    return [iD,token]