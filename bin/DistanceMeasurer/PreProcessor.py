''' Created on Jan 17, 2014, @author: schiklen '''

# python imports
from os import path
import pickle
import re

# ImageJ imports
from emblcmci.foci3Dtracker import PreprocessChromosomeDots as Preprocessor
from ij.io import OpenDialog, Opener
from ij.plugin import RGBStackMerge as StackMerge
from ij.plugin.filter import Filler as CO
import ij.plugin.ChannelSplitter as CS
from ij.process import ImageConverter

from containers import experiment, position, cell, frame, dot



def preprocess(cell):
    print cell.getRawImageFilePath()
    imp = Opener().openImage(cell.getRawImageFilePath()) # open raw Image
    #if imp.getBitDepth() != 8:  # converting to 8 bit if 
    #   ImageConverter(imp).convertToGray8()
    roi = imp.roi
    imps = CS.split(imp)
    p = Preprocessor()
    for aimp in imps:
        p.setImp(aimp)
        p.run()
        if roi != None:
            aimp.setRoi(roi)
            for n in range(1, aimp.getImageStackSize()+1):
                aimp.getImageStack().getProcessor(n).fillOutside(roi)
            aimp.killRoi()
        final = StackMerge.mergeChannels(imps, False)
        final.copyScale(imp) # copyscale from .copyscale
    return final


#---- M A I N ----

od = OpenDialog("Open Experiment!", "") # string head, string default path
loadFile = open(path.join(od.getDirectory(), od.getFileName()))
experiment = pickle.load(loadFile)

c = experiment.getPositions()[0].getCells()[0]

preprocess(c)

'''
for p in experiment.getPositions():
    for c in p.getCells():
        print c.getPosition().getID(), c.getID()
        print c.getRawImageFilePath()
        if c.isPreProcessed() == False:
            preprocess(c)
'''
