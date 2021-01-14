from ncTCPServer import ncTCPServer
import time

extracted = None


def useData(data, name):
    print("Got data as ", data)
    if data == b"Hello\n":
        print("Send Hello to client")
        ncTS.write(packetCreate(b"Hello From Server!"))
        return True # Continuation expected
    elif data == b"Hello From Client!\n":
        print("Test Passed!")
        print("Got Hello from client!")
        ncTS.stop()
        exit(0)
    if name is not None:
        print("Got name as", name)
    return False


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
            if useData(extracted, name):
                return None
            return True
        else:
            print(size - recivedLength - 1)
            return size - recivedLength - 1
    return False


def packetCreate(data, name=None):
    packet = str(len(data)).encode()
    packet += b":"
    if (name != None):
        packet += name
        packet += b":"
    packet += b"E:"
    packet += data
    packet += b"\n"
    return packet


ncTS = ncTCPServer()
print("Started server...")
ncTS.action = packetCheck
if not ncTS.test():
    print("ERROR: Something went sideways! Netcat thread exited prematurely!")
    exit(-1)
print("Joining with server thread..")
ncTS.join()
