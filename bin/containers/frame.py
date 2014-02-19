'''
Created on Nov 18, 2013
@author: schiklen
'''

class frame(object):
    '''frame object'''

    def __init__(self, ID, time, distance, x1, y1, z1, x2, y2, z2):
        '''Constructor'''
        
        self.ID = ID
        self.time = time
        self.distance = distance
        self.x1, self.y1, self.z1 = x1, y1, z1
        self.x2, self.y2, self.z2 = x2, y2, z2
        
        self.dots = []
        
        self.isAnaphaseOnset = False
        self.isCytokinesis = False
        
        
    def setAnaphaseOnset(self, z):
        self.isAnaphaseOnset = z
        
    def setCytokinesis(self, z):
        self.isCytokinesis = z
        
    def getXYZasTuple(self, channel):
        if channel == 1:
            return self.x1, self.y1, self.z1
        if channel == 2:
            return self.x2, self.y2, self.z2