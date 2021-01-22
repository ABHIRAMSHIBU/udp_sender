from ncUDPClient import ncUDPClient
from ncTCPClient import ncTCPClient
from fileHash import FileHash
from FileTree import fileTree
from packetFactory import packetFactory
import json

# This is the client because its the sender.
index = 0

def argParse():
    import sys
    argv = sys.argv
    args = {"tcpport": 5006, "udpport": 5005, "ip": "127.0.0.1", "file": "testfiles/test.png"}
    for i in range(len(argv)):
        if (i == 0):
            continue
        if ((argv[i] == "--tcpport") or (argv[i] == "-tp")):
            try:
                args["tcpport"] = int(argv[i + 1])
            except IndexError:
                print("Catastrophic Failure, please give tcp port")
                exit(-1)
        elif ((argv[i] == "--udpport") or (argv[i] == "-up")):
            try:
                args["udpport"] = int(argv[i + 1])
            except IndexError:
                print("Catastrophic Failure, please give udp port")
                exit(-1)
        elif ((argv[i] == "--host") or (argv[i] == "-h")):
            try:
                args["ip"] = str(argv[i + 1])
            except IndexError:
                print("Catastrophic Failure, please give udp port")
                exit(-1)
        elif ((argv[i] == "--file") or (argv[i] == "-f")):
            try:
                args["file"] = str(argv[i + 1])
            except IndexError:
                print("Catastrophic Failure, please give udp port")
                exit(-1)
        elif ((argv[i] == "--help") or (argv[i] == "-h")):
            print('''UDP Sender Alpha V1.0
    -tp or --tcpport is used to set tcp port
    -up or --udpport is used to set udp port
    -h  or --host    is used to set host ip
    -f  or --file    is used to set which file to send
Example
    ''' + argv[0] + ''' -tp 5006 -up 5005 -h 192.168.1.2''')
            exit(0)
    return args


args = argParse()        # Get arguments from the user
print(args)


def useData(data, name):
    global index
    #print("Got data as ", data)
    node = tree.getNode(index)
    #sequence, packet = pf.create(node)
    #print(node)
    packet = node
    if data == b"OK\n":
        index+=1
        print("OK",index-1)
        ncUC.write(packetCreate(packet, name=str(index-1)))
        #print(packet)
        return True
    elif data == b"ACK\n":
        index+=1
        print("ACK",index-1)
        ncUC.write(packetCreate(packet, name=str(index-1)))
        #print(packet)
        return True
    elif data == b"NACK\n":
        node = tree.getNode(index-1)
        sequence, packet = pf.create(node)
        #print(node)
        packet = node
        print("NACK",index-1)
        ncUC.write(packetCreate(packet, name=str(index-1)))
        #print(packet)
        return True
    elif data == b"DONE\n":
        print("Got DONE from server!")
        ncTC.write(b"DONE")
        ncUC.write(b"DONE")
        ncTC.stop()
        ncUC.stop()
        ncTC.process.kill()
        ncUC.process.kill()
        return False
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
            if useData(extracted, name):
                return None
            return True
    return False


def packetCreate(data, name=None):
    packet = str(len(data)).encode()
    packet += b":"
    if (name != None):
        packet += name.encode()
        packet += b":"
    packet += b"E:"
    packet += data
    packet += b"\n"
    return packet

# Create clients
ncUC = ncUDPClient(port=args["udpport"], ip=args["ip"])
ncTC = ncTCPClient(port=args["tcpport"], ip=args["ip"])
ncTC.setAction(packetCheck)
# Need to get file as hash
chunksize = 1000
fh = FileHash(chunksize, args["file"], generate=True)
pf = packetFactory()
# Generate tree from file
tree = fileTree(args["file"],chunksize)
# print(fh.MD5) # MD5 Sum is OK
MD5 = fh.MD5
MD5.append(args["file"][args["file"].rindex("/")+1:])
# Send hash
ncTC.write(packetCreate(json.dumps(fh.MD5).encode(),"MD5"))

#ncUC.write(packetCreate(packet,name=str(sequence)))
# Kill all connections just for now..
# ncUC.stop()
# ncTC.stop()
# ncUC.process.kill()
# ncTC.process.kill()



