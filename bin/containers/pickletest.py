'''
Created on Jan 23, 2014

@author: schiklen
'''

import pickle



class A(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        #self.a = a
        self.listOfBs = []
        
    def addB(self, b):
        self.listOfBs.append(b) 
        
class B(object):
    def __init__(self, c):
        self.c = c
        
        
# -- main

f = A()

for i in range(5):
    n = B(i)
    f.addB(n)
    
print f.listOfBs

dumpFile = 
    