#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 13 16:34:40 2020

@author: Anjali Venugopal
@secondary-author: Abhiram Shibu
"""

class Queue():
    '''Needs size as an optional argument, if not defined size becomes unlimitted'''
    def __init__(self,size=0):
        self.queue = []
        self.size = size
        if(size==0):
            self.NoLimit=True
        else:
            self.NoLimit=False
    def __str__(self):
        myString = ' '.join(str(i) for i in self.queue)
        return myString

        
    def enqueue(self, item):
        '''This function adds an item to the rear end of the queue '''
        if(self.isFull() != True):
            self.queue.insert(0, item)
        else:
            return -1 # Queue is FULL

    def dequeue(self):
        ''' This function removes an item from the front end of the queue '''
        if(self.isEmpty() != True):
            return self.queue.pop()
        else:
            return None # Can't dequeue, Q empty

    def isEmpty(self):
        ''' This function checks if the queue is empty '''
        return self.queue == []

    def isFull(self):
        ''' This function checks if the queue is full '''
        if(self.NoLimit):
            return False
        else:
            return len(self.queue) == self.size

    def peek(self):
        ''' This function helps to see the first element at the fron end of the queue '''
        if(self.isEmpty() != True):
            return self.queue[-1]
        else:
            return None # Can't peek, Q empty

