#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 13 22:34:35 2020

@author: abhiram
"""
import time
import UDPClient
import TCPClient

def argParse():
    import sys
    argv = sys.argv
    args = {"tcpport":5006,"udpport":5005,"ip":"127.0.0.1"}
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
        elif((argv[i]=="--host") or (argv[i]=="-h")):
            try:
                args["ip"]=int(argv[i+1])
            except IndexError:
                print("Catastrophic Failure, please give udp port")
                exit(-1)
        elif((argv[i]=="--help") or (argv[i]=="-h")):
            print('''UDP Sender Alpha V1.0
    -tp or --tcpport is used to set tcp port
    -up or --udpport is used to set udp port
    -h  or --host    is used to set host ip
Example
    '''+argv[0]+''' -tp 5006 -up 5005 -h 192.168.1.2''')
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
args=argParse()
print(args)
uc=UDPClient.udp(args["udpport"],args["ip"])
pattern=generator(10)
tc=TCPClient.tcpClient(args["ip"],args["tcpport"])
tc.asyncRead(delay=0.05)
try:
    while True:
        print("Send")
        uc.send(pattern)
        counter=5
        while tc.avilable()==0:
            counter-=1
            if(counter==0):
                break
            time.sleep(0.01)
        if(counter!=0):
            print(tc.read())
        else:
            print("Error")
        time.sleep(0.05)
except KeyboardInterrupt:
    pass