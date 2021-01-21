#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 16 12:31:19 2021

@author: jerome
"""

import subprocess as sp


while(True):
    c=input("test UDP \n1.image 2.video 3.text 4.raw \ntest TCP \n5.image 6.video 7.text 8.raw\n")
    if (int(c)==1):
        process = sp.Popen("nc -lp 6001 >lowerrww " , shell=True)
        process = sp.Popen("nc localhost 6001 < new " , shell=True)
    if (int(c)==2):
        process = sp.Popen("nc -lp 6001 >lowerrww.jpg " , shell=True)
        process = sp.Popen("nc localhost 6001 < 1.png " , shell=True)
    

    else:
        break