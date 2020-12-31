#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 13 22:34:35 2020

@author: abhiram
"""
import time
import UDPClient
import TCPClient
from fileHash import FileHash
from packetFactory import packetFactory

pf = packetFactory()


def argParse():
    import sys
    argv = sys.argv
    args = {"tcpport": 5006, "udpport": 5005, "ip": "127.0.0.1", "file": "/tmp/test"}
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
        elif ((argv[i] == "--file") or (argv[i] == "-f")):
            try:
                args["file"] = argv[i + 1]
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


def generator(l):
    '''Returns length sized pattern'''
    import math
    basicBlock = b"1011"
    output = (basicBlock * math.ceil(l / len(basicBlock)))[:l]
    return output


def packetSizeTest(args):
    pf = packetFactory()
    uc = UDPClient.udp(args["udpport"], args["ip"])
    size = 1
    tc = TCPClient.tcpClient(args["ip"], args["tcpport"])
    tc.asyncRead(delay=0.00005)
    try:
        while True:
            pattern = generator(size)
            sequence, packet = pf.create(pattern)
            print("Send packet with sequence number ", sequence)
            uc.send(packet)
            counter = 100
            while tc.avilable() == 0:
                counter -= 1
                if counter == 0:
                    break
                time.sleep(0.00001)
            if counter != 0:
                result = tc.read().decode().strip()
                print(result)
                if "ACK" in result[:3]:
                    result = int(result.replace("ACK_", ""))
                    if result == size:
                        print("Verified ", size)
                        size += 1
                    else:
                        print("Verification Failure")
                        print(size)
                        break
                elif "NACK" in result[:4]:
                    print("Max Size is ", size - 1)
                    break
                print()
            else:
                print("Error")
            time.sleep(0.00005)
    except KeyboardInterrupt:
        pass


args = argParse()


def chunkToPacket(chunk, chunkSize, packetSize):
    import math
    packetsSequnce = []
    for i in math.ceil(chunkSize / packetSize):
        start = packetSize * i
        end = start + packetSize
        packet = chunk[start:end]
        packetsSequnce.append(pf.create(packet))
    return packetsSequnce


def md5SumSend(args, chunksize, tc):
    import pickle
    file = args["file"]
    fh = FileHash(chunksize, file, generate=True)
    md5list = fh.getMD5()
    print(md5list)
    data = pickle.dumps(md5list)
    print(data)
    tc.send(data)

print(args)
#uc = UDPClient.udp(args["udpport"], args["ip"])
size = 1
tc = TCPClient.tcpClient(args["ip"], args["tcpport"])
tc.asyncRead(delay=0.00005)
md5SumSend(args,100,tc)
print("Done")
tc.stop()
exit(0)