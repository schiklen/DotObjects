''' Created on Jan 17, 2014, @author: schiklen '''

# ImageJ imports
from emblcmci.foci3Dtracker import PreprocessChromosomeDots as Preprocessor
from ij.io import OpenDialog, Opener
from ij.plugin import RGBStackMerge, ChannelSplitter

# Java imports
import java.lang.IllegalArgumentException

# Python imports
from os import path
import pickle


def preprocess(cell):
    print cell.getRawImageFilePath()
    imp = Opener().openImage(cell.getRawImageFilePath()) # open raw Image
    #if imp.getBitDepth() != 8:  # converting to 8 bit if 
    #   ImageConverter(imp).convertToGray8()
    roi = imp.roi
    imps = ChannelSplitter().split(imp)
    p = Preprocessor()
    for aimp in imps:
        p.setImp(aimp)
        p.run()
        if roi != None and roi.isArea(): # and (invertroi area = 0):
            aimp.setRoi(roi)
            for n in range(1, aimp.getImageStackSize()+1):
                try:
                    aimp.getImageStack().getProcessor(n).fillOutside(roi)
                except java.lang.IllegalArgumentException:   # if the roi covers the complete image, fillOutside(roi) throws an error.
                    pass
            aimp.killRoi()
        else:
            print "No area roi present."
        #aimp.close()
        
    final = RGBStackMerge.mergeChannels(imps, False)
    for imp in imps:
        imp.close()
    final.copyScale(imp) # copyscale from .copyscale
    return final


#---- M A I N ----

od = OpenDialog("Open Experiment!", "") # string head, string default path
loadFile = open(path.join(od.getDirectory(), od.getFileName()))
experiment = pickle.load(loadFile)

#c = experiment.getPositions()[0].getCells()[1]

for p in experiment.getPositions():
    for c in p.getCells():
        print c.getPosition().getID(), c.getID()
        print c.getRawImageFilePath()
        if c.isPreProcessed() == False:
            ppcdImp = preprocess(c)
            #save preprocessed image under ppcd path
            c.saveImp(c.getPpcdImageFilePath(), ppcdImp)

