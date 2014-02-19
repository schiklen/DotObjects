'''
Created on Nov 18, 2013
@author: schiklen
'''

from frame import frame
from os import path, mkdir
import CONSTANTS as C
from ij import IJ
from ij.gui import Roi

class cell(object):
    '''classdocs'''

    def __init__(self, position, ID, rawImageDir, rawImp): #, x, y):
        '''Constructor'''

        self.position = position
        self.ID = ID  # id is also roiName
        self.rawImageDir = str(rawImageDir)
        self.rawImageFileName = "p" + str(self.position.getID()) + "_c" + str(self.ID)
        self.rawImageFilePath = path.join(self.rawImageDir, (self.rawImageFileName + ".tiff"))
        self.saveImp(self.rawImageFilePath, rawImp)

        self.ppcdImageDir = path.join(path.split(rawImageDir)[0], C.PPCD_DIR)
        self.ppcdImageFileName = C.PREPROCESSED_PREFIX + self.rawImageFileName
        self.ppcdImageFilePath = path.join(self.ppcdImageDir, (self.ppcdImageFileName + ".tiff"))
        
        self.measImageDir = path.join(path.split(rawImageDir)[0], C.MEAS_DIR)
        self.measImageFileName = C.MEASUREDIMAGE_PREFIX + self.rawImageFileName
        self.measImageFilePath = path.join(self.measImageDir, (self.measImageFileName + ".tiff"))

        self.frames = []
        self.phenoype = None

    def __getstate__(self): # set pickling options: overlay and imp not serialized!
        state = dict(self.__dict__)
        return state

        
    def saveImp(self, filePath, imp):
        cDir = path.split(filePath)[0]
        if not path.exists(cDir):
            print "Making directory " + cDir
            mkdir(cDir)
        IJ.saveAs(imp, ".tiff", filePath)
        print "Saved as " + filePath + ".tiff"

    def getRoiInPosition(self):
        return self.roiInPosition
        
    def addFrame(self,frame):
        self.frames.append(frame)
        
    def getFrames(self):
        return self.frames
    
    def setPhenotype(self, phenotype):
        self.phenoype = phenotype
    
    def getPhenotype(self):
        return self.phenotype
        
    def getID(self):
        return self.ID
    
    def getPosition(self):
        return self.position
    
    def getRawImageFilePath(self):
        return self.rawImageFilePath
    
    def getPpcdImageFilePath(self):
        return self.ppcdImageFilePath
    
    def isPreProcessed(self):
        if path.exists(self.ppcdImageFilePath):
            return True
        else:
            return False
    
                    #remove(cell.getMeasImageFilePath())
                #remove(cell.getMeasValFilePath())
                #remove(cell.getqcValFilePath())