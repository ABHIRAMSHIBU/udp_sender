#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 13 16:03:02 2020

@author: Vishnu
@secondary-author: Abhiram Shibu
"""

class stack:
    def __init__ (self):
        from collections import deque
        self.container=deque()
    def push(self,val):
        self.container.append(val)
    def pop(self,handle=False):
        '''Will raise IndexError if empty.'''
        if(handle):
            value=None
            try:
                value=self.container.pop()
            except IndexError:
                pass
            return value
        else:
            return self.container.pop()
    def peek(self):
        return self.container[-1]
    def is_empty(self):
        return len(self.container)==0
    def size(self):
        return len(self.container)