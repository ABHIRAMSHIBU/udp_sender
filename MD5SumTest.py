#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 13 18:19:58 2020

@author: Anandakrishnan P 
@secondary-author: Abhiram Shibu
"""
from MD5Sum import CheckSum
from os import popen
txt="Hello"
data1=CheckSum.get_md5(txt)
data=popen("printf "+txt+" 2>&1 | md5sum | awk '{print $1}'").read()
if(str(data1.strip())==str(data.strip())):
    print("Test Pass!")
else:
    print("Test Failed")
print(data)
