'''
Created on Feb 16, 2014

@author: schiklen
'''

''' Created on Jan 17, 2014, @author: schiklen '''

# ImageJ imports
from emblcmci.foci3Dtracker import AutoThresholdAdjuster3D as ATA
from ij.io import OpenDialog, Opener
from ij.plugin import RGBStackMerge, ChannelSplitter

# Java imports
import java.lang.IllegalArgumentException

# Python imports
from os import path
import pickle


def measure(cell):
    print "Opening", cell.getPpcdImageFilePath()
    imp = Opener().openImage(cell.getPpcdImageFilePath()) # open preprocessed Image
    imps = ChannelSplitter.split(imp)
    a = ATA()
    a.setSilent(True)
    a.segAndMeasure(imps[0], imps[1])
    results = a.getLinkedArray()
    print results
    
    

#---- M A I N ----

od = OpenDialog("Open Experiment!", "") # string head, string default path
loadFile = open(path.join(od.getDirectory(), od.getFileName()))
experiment = pickle.load(loadFile)

c = experiment.getPositions()[0].getCells()[1]

measure(c)

'''for p in experiment.getPositions():
    for c in p.getCells():
        print c.getPosition().getID(), c.getID()
        print c.getRawImageFilePath()
        if c.isPreProcessed() == False:
            ppcdImp = preprocess(c)
            #save preprocessed image under ppcd path
            c.saveImp(c.getPpcdImageFilePath(), ppcdImp)'''

