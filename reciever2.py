#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 13 22:11:47 2020

@author: Abhiram Shibu
@Co-author: Jerome Joseph
"""
# GOLBAL IMPORTS
import UDPServer
import TCPServer
import time
from packetFactory import packetFactory

# END GLOBAL IMPORTS

# GLOBAL VARIABLES
DELAY = 0.00005
pf = packetFactory()


# END GLOBAL VARIABLES


# GLOBAL FUNCTIONS
def argParse():
    '''Parses arguments and returns a dictionary'''
    import sys
    argv = sys.argv
    args = {"tcpport": 5006, "udpport": 5005}
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
        elif ((argv[i] == "--help") or (argv[i] == "-h")):
            print('''UDP Reciver Alpha V1.0
    -tp or --tcpport is used to set tcp port
    -up or --udpport is used to set udp port
Example
    ''' + argv[0] + ''' -tp 5006 -up 5005''')
            exit(0)
    return args


def generator(l):
    '''Returns length sized pattern'''
    import math
    basicBlock = b"1011"
    output = (basicBlock * math.ceil(l / len(basicBlock)))[:l]
    return output


# END GLOBAL FUNCTIONS
def packetSizeTest(args):
    pf = packetFactory()
    us = UDPServer.udp(args["udpport"], "127.0.0.1")
    ts = TCPServer.tcpServer("127.0.0.1", args["tcpport"])
    ts.start()
    tcpclient = ts.acceptConnection()
    us.recieve()

    while (True):
        while (us.available() == 0):
            time.sleep(DELAY)
        data = us.read()
        try:
            sequence, data = pf.open(data)
        except:
            print("Error decoding packet")
            tcpclient.send(b"NACK_" + str(None).encode() + b"\n")
            continue
        pattern = generator(len(data))
        if (data == pattern):
            print(pattern)
            print("Perfect! Sequence number ", sequence)
            tcpclient.send(b"ACK_" + str(len(data)).encode() + b"\n")
        else:
            # print(b"NACK_"+str(len(data)).encode()+b"\n")
            tcpclient.send(b"NACK_" + str(len(data)).encode() + b"\n")


def md5SumRecv(args, chunksize, tcpclient):
    import time
    import pickle
    totalData=b""
    masterCounter=0
    while(True):
        #print("Waiting for packets")
        count=0
        while(tcpclient.available()==0):
            count+=1
            time.sleep(0.0005)
            if(count==10000):
                break
        #print("Got something")
        data=tcpclient.readKeep()
        if(len(data)==len(totalData)):
            masterCounter+=1
            if(masterCounter==10000):
                #print("Hope this is it..")
                break
        else:
            pass
            #print(len(data),len(totalData),masterCounter)
        totalData=data
        time.sleep(0.0005)
        if(count==10000):
            #print("All waits over.. now real processing..")
            break
    with open("/tmp/output.jpg","wb") as f:
        f.write(totalData)
        f.close()
    tcpclient.read()
    #md5list=pickle.loads(totalData)
    #return md5list

args = argParse()
print(args)
ts = TCPServer.tcpServer("127.0.0.1", args["tcpport"])
ts.start()
tcpclient = ts.acceptConnection()
tcpclient.recieve()
print(md5SumRecv(args,100,tcpclient))
tcpclient.stop()
exit(0)
