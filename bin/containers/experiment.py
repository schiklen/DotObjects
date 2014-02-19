'''
Created on Nov 17, 2013
@author: schiklen
'''

from position import position
from os import path, listdir, makedirs
#from datetime import date
import re
import CONSTANTS as C
import cPickle

class experiment(object):

    def __init__(self, dirPath, Date, strain, temperature, startOD, condition):
        '''Make an experiment object'''
     
        if path.exists(dirPath):
            self.dirPath = dirPath
            self.basePath = path.split(dirPath)[0]
        else:
            raise IOError("Input Error: Path of experiment data not found!")

        self.ppcdFolder = path.join(self.basePath,C.PPCD_DIR)
        self.cutoutFolder = path.join(self.basePath,C.CUTOUT_DIR)
        self.measFolder = path.join(self.basePath,C.MEAS_DIR)
        self.qcmeasFolder = path.join(self.basePath,C.QCMEAS_DIR)
        
        self.date = Date
        self.strain = strain
        self.temp = temperature
        self.startOD = startOD
        self.condition = condition

        self.currPosCounter = 0
        self.posCounter = 0
        self.positions = []
        self.makePositions(self.dirPath)

        if self.positions != []:
            self.currPos = self.positions[self.currPosCounter]
        else:
            raise IOError("No positions found!")
        
        self.qualityChecked = False
        self.analysisFolder = path.join(self.basePath, C.ANALYSIS_DIR)
        self.serialFileName = str(self.date) + "_" + str(self.strain) + ".exp"
        self.serialFilePath = path.join(self.analysisFolder, self.serialFileName)
                    
    def serialize(self):
        try:
            makedirs(self.analysisFolder)
        except OSError:
            #ask, if overwrite!
            print "Overwriting existing serialization"
        f = open(self.serialFilePath, "w")
        cPickle.dump(self, f)
        f.close()
        
    def exportDataAsCsv(self, exportPath):
        if self.qualityChecked == True:
            print "Here: export as complete tsv"
            '''csv = file.open(exportPath, rw)
            for p in self.positions:
                for c in p.getCells():
                    for f in c.getFrames():
                    csv.writeLine(self.Date + "," + self.strain + "," + self.temp + "," + self.startOD + "," + self.condition 
                                  + "," + p.getID()
                                  + "," + c.getID()
                                  + "," + f.getID() + "," + f.getTime() + "," + )
                    '''
            
            
    # --- All that position stuff ---
    def makePositions(self, rawFolder):
        ''''''
        allFiles = listdir(rawFolder)
        isDVorTIF = re.compile('(?P<prefix>.+)(?P<suffix>\.tif|\.dv)$')
        onlyDVTIF = [isDVorTIF.match(f).group(0) for f in allFiles if isDVorTIF.match(f)]
        posID = 1
        for p in onlyDVTIF:
            q = position(path.join(self.dirPath,p), posID) #initial construction of positions.
            self.addPosition(q)
            posID += 1

    def addPosition(self, pos):
        self.positions.append(pos)
    
    def getPositions(self):
        return self.positions

    def setCurrPos(self, ID):
        self.currPos = self.positions[ID]
    
    def incrementPos(self):
        if self.currPosCounter < (len(self.positions)-1):
            self.currPosCounter += 1
            self.currPos = self.positions[self.currPosCounter]
        else:
            print "Last Position."
    
    def decrementPos(self):
        if self.currPosCounter > 0:
            self.currPosCounter -= 1
            self.currPos = self.positions[self.currPosCounter]
        else:
            print "First position!"
    
    def getCurrPos(self):
        return self.currPos
