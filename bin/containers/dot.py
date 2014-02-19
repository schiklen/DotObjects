'''Created on Jan 15, 2014,@author: schiklen'''


class dot(object):
    '''A dot object, bitches!'''


    def __init__(self, channel, x, y, z, intensity, volume):
        '''        Constructor        '''
        
        self.channel = channel
        self.x = x
        self.y = y
        self.z = z
        self.intensity = intensity
        self.volume = volume