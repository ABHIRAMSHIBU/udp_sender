from ncTCPClient import ncTCPClient
import time
import os

extracted = None


def useData(data, name):
    print("Got data as ", data)
    if data == b"OK\n":
        print("Got OK from server!")
        ncTC.run=False
        exit(0)
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


args = argParse()
print(args)

if "recived" not in os.listdir():
    os.mkdir("recived")

#Determining file name
fname = args["file"].split("/")[-1]


ncTC = ncTCPClient(port=args["tcpport"], ip=args["ip"])
time.sleep(0.5)
ncTC.action = packetCheck
#data=open("testfiles/test.png","rb").read()
data=open(args["file"],"rb").read()
ncTC.write(packetCreate(data,fname))
print("Send file as ",fname)
ncTC.join()
