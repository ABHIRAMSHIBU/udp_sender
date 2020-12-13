#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 13 15:46:04 2020

@author: abhiram
"""

from TCPClient import tcpClient
tc=tcpClient("127.0.0.1", 7011)
tc.send("Hello World!")
tc.close()
print("You should be seeing hello world in server")