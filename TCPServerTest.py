#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 13 15:39:36 2020

@author: Abhiram Shibu
"""

import TCPServer
ts=None
try:
    ts = TCPServer.tcpServer()
    ts.start()
    u = ts.acceptConnection()
    while(True):
        c=input("1) Check Available Data \n2) Read Available Data\n0) Exit\nenterchoice:")
        if (int(c)==1):
            print(u.available())
        elif(int(c)==2):
            print(u.read())
        else:
            break
    u.stop()
    ts.close()
except KeyboardInterrupt:
    u.stop()
    ts.close()
    print("Keyboard interrupt! Exiting")
    