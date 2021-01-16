from ncUDPServer import ncUDPServer
import time,os

extracted = None

def argParse():
    import sys
    argv = sys.argv
    args = {"tcpport": 5006, "udpport": 5005, "ip": "127.0.0.1", "dir": "recived/"}
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
                args["ip"] = int(argv[i + 1])
            except IndexError:
                print("Catastrophic Failure, please give udp port")
                exit(-1)
        elif ((argv[i] == "--dir") or (argv[i] == "-d")):
            try:
                args["dir"] = str(argv[i + 1])
            except IndexError:
                print("Catastrophic Failure, please give udp port")
                exit(-1)
        elif ((argv[i] == "--help") or (argv[i] == "-h")):
            print('''UDP Sender Alpha V1.0
    -tp or --tcpport is used to set tcp port
    -up or --udpport is used to set udp port
    -h  or --host    is used to set host ip
    -d  or --dir    is used to set the recieve directory
Example
    ''' + argv[0] + ''' -tp 5006 -up 5005 -h 192.168.1.2''')
            exit(0)
    return args

args = argParse()
print(args)

def useData(data, name):
    global args
    fdir=args["dir"]
    if(fdir[-1]!="/"):
        fdir+="/"
    #print("Got data as ", data)
    if name:
        if os.path.exists(fdir):
            if not os.path.isdir(fdir):
                print("ERROR: Path specified is a file!")
                exit(-1)
        else:
            os.mkdir(fdir)
        f = open(fdir + name.decode(), "wb")
        f.write(data[:-1])
        f.close()
        print("Success.. Recived file", name)
        ncUS.write(packetCreate(b"OK"))
        ncUS.stop()
        exit(0)
    # if data == b"Hello\n":
    #     print("Send Hello to client")
    #     ncTS.write(packetCreate(b"Hello From Server!"))
    #     return True # Continuation expected
    # elif data == b"Hello From Client!\n":
    #     print("Test Passed!")
    #     print("Got Hello from client!")
    #     ncTS.stop()
    #     exit(0)
    # if name is not None:
    #     print("Got name as", name)
    # return False


def packetCheck(data):
    # Example Packet b"5:E:Hello" <- endSig = sizeSign
    # Example File b"5:Name:E:Hello" <- endSig > sizeSign
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
            #print(size - recivedLength + 1)

            chunksize=min(int((size - recivedLength + 1)/2),min(max(4096,int(size/20)),200000000))
            return chunksize
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

ncUS = ncUDPServer(args["udpport"])
print("Started server...")
ncUS.action = packetCheck
if not ncUS.test():
    print("ERROR: Something went sideways! Netcat thread exited prematurely!")
    exit(-1)
print("Joining with server thread..")
ncUS.join()
