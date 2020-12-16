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
# END GLOBAL VARIABLES 


# GLOBAL FUNCTIONS
def argParse():
    '''Parses arguments and returns a dictionary'''
    import sys
    argv = sys.argv
    args = {"tcpport":5006,"udpport":5005}
    for i in range(len(argv)):
        if(i==0):
            continue
        if((argv[i]=="--tcpport") or (argv[i]=="-tp")):
            try:
                args["tcpport"]=int(argv[i+1])
            except IndexError:
                print("Catastrophic Failure, please give tcp port")
                exit(-1)
        elif((argv[i]=="--udpport") or (argv[i]=="-up")):
            try:
                args["udpport"]=int(argv[i+1])
            except IndexError:
                print("Catastrophic Failure, please give udp port")
                exit(-1)
        elif((argv[i]=="--help") or (argv[i]=="-h")):
            print('''UDP Reciver Alpha V1.0
    -tp or --tcpport is used to set tcp port
    -up or --udpport is used to set udp port
Example
    '''+argv[0]+''' -tp 5006 -up 5005''')
            exit(0)
    return args
def generator(l):
    '''Returns length sized pattern'''
    n=b""
    basicBlock=b"1011"
    for i in range(0,l,len(basicBlock)): # evade the use of costly modulo operator
        actual=0
        for j in range(len(basicBlock)):
            actual=i+j
            if(actual==l):
                break
            n+=basicBlock[j:j+1]
        if(actual==l):
            break
    return n
# END GLOBAL FUNCTIONS

args=argParse()
print(args)

pf = packetFactory()

us=UDPServer.udp(args["udpport"],"127.0.0.1")
ts=TCPServer.tcpServer("127.0.0.1",args["tcpport"])
ts.start()
tcpclient = ts.acceptConnection()
us.recieve()

while(True):
    while(us.available()==0):
        time.sleep(DELAY)
    data=us.read()
    try:
        sequence,data=pf.open(data)
    except:
        print("Error decoding packet")
        tcpclient.send(b"NACK_"+str(None).encode()+b"\n")
        continue
    pattern=generator(len(data))
    if(data==pattern):
        print(pattern)
        print("Perfect! Sequence number ",sequence)
        tcpclient.send(b"ACK_"+str(len(data)).encode()+b"\n")
    else:
        #print(b"NACK_"+str(len(data)).encode()+b"\n")
        tcpclient.send(b"NACK_"+str(len(data)).encode()+b"\n")