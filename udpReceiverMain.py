from ncTCPServer import ncTCPServer
from ncUDPServer import ncUDPServer
from time import sleep
from signal import signal
import json
from threading import Semaphore
from packetFactory import packetFactory
from MD5Sum import CheckSum
from Queue import Queue
# This is the server because it is going to receive the file bring send.
RECVALL=True # True means it will receive all packets...
MD5=None
OLDMD5=[]
index=0
totalSize = 0
semaphore = Semaphore(1)
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
outputFile = open("/tmp/test.png", "wb")
def useData(data, name):
    global args
    global MD5
    global index
    global outputFile
    global totalSize
    semaphore.acquire()
    fdir=args["dir"]
    if(fdir[-1]!="/"):
        fdir+="/"
    #print("Got data as ", data)
    # if name:
    #     if os.path.exists(fdir):
    #         if not os.path.isdir(fdir):
    #             print("ERROR: Path specified is a file!")
    #             exit(-1)
    #     else:
    #         os.mkdir(fdir)
    #     f = open(fdir + name.decode(), "wb")
    #     f.write(data[:-1])
    #     f.close()
    #     print("Success.. Recived file", name)
    #     ncUS.write(packetCreate(b"OK"))
    #     ncUS.stop()
    #     exit(0)
    if(name==b"MD5"):
        print("In:MD5")
        MD5=json.loads(data)
        if(RECVALL==True):
            ncTS.write(packetCreate(b"SNDALL"))
        else:
            ncTS.write(packetCreate(b"OK"))
        outputFile=open(fdir+MD5.pop(-1),"wb")
        Q = Queue()
        totalSize = len(MD5)
        while(len(MD5)):
            Q.enqueue(MD5.pop(0)[0])
        MD5=Q
        #print("MD5 is now a Q")
        # ncTS.stop()
        # exit(0)
    else:
        print("In:DP")
        #print(name)
        #print(data[:-1])
        cs=CheckSum(data[:-1])
        nodeMD5 = MD5.dequeue()
        OLDMD5.append(nodeMD5)
        if(cs.verify_md5(nodeMD5)):
            #print("MD5 OK!")
            if(not RECVALL):
                ncTS.write(packetCreate(b"ACK"))
            outputFile.write(data[:-1])
            index+=1
            if(index==totalSize):
                ncTS.write(packetCreate(b"DONE"))
                ncUS.write(packetCreate(b"DONE"))
                ncTS.stop()
                ncUS.stop()
                ncTS.process.kill()
                ncUS.process.kill()
                outputFile.close()
                exit(0)
        else:
            #print("MD5 Failed verification!")
            ncTS.write(packetCreate(b"NACK",index))
            exit(0)
    semaphore.release()
    return True




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

args = argParse()
print(args)


# Start server
ncUS = ncUDPServer(args["udpport"])
ncTS = ncTCPServer(args["tcpport"])
ncTS.setAction(packetCheck)
ncUS.setAction(packetCheck)


#There are two ways to wait
# while(ncTS.run):   # Sleeping with while
#     sleep(0.001)
ncTS.join()
# Kill server
# ncUS.stop()
ncTS.stop()
ncTS.process.kill()
# ncUS.process.kill()


