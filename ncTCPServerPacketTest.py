from ncTCPServer import ncTCPServer
import time

extracted = None


def useData(data, name):
    print("Got data as ", data)
    if data == b"Hello\n":
        print("Send Hello to server")
        ncTS.write(packetCreate(b"Hello From Server!"))
    if name is not None:
        print("Got name as", name)


def packetCheck(data):
    # Example Packet b"5:E:Hello"
    global extracted
    global name
    try:
        endSignaturePointer = data.index(b":E:")
        sizeSignaturePointer = data.index(b":")
        name = None
    except ValueError:
        return False
    if endSignaturePointer != -1:
        size = int(data[:sizeSignaturePointer].decode())
        if sizeSignaturePointer != endSignaturePointer:  # A name section also exists
            name = data[sizeSignaturePointer + 1:endSignaturePointer]
        signatureSize = endSignaturePointer + 3
        recivedLength = len(data) - signatureSize
        if recivedLength - 1 == size:
            extracted = data[signatureSize:]
            useData(extracted, name)
            return True
    return False

def packetCreate(data,name=None):
    packet = str(len(data)).encode()
    packet += b":"
    if(name!=None):
        packet += name
        packet += b":"
    packet += b"E:"
    packet += data
    packet += b"\n"
    return packet

ncTS = ncTCPServer()
ncTS.action = packetCheck
ncTS.join()
