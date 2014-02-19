'''
A GUI DotAssay data extraction routine
Christoph Schiklenk, 2013/2014
schiklen@embl.de
'''

from containers.experiment import experiment
from containers.position import position
from containers.cell import cell
from containers.frame import frame
from containers import CONSTANTS as C
from os import path
import gui, CropperGui
import cPickle


def okayEvent(event):
    pth, date, strain, temp, OD, cond = dial.getValues()
    mainDir = path.split(path.split(pth)[0])[0] 
    experimentPath = path.join(path.join(mainDir, C.ANALYSIS_DIR), str(date) + "_" + str(strain) + ".exp")
    imgFilePath = path.split(pth)[0]
    #if not there, pickle and make experiment, otherwise load other ex
    if path.exists(experimentPath):
        print "Loading experiment file", experimentPath
        loadFile = open(experimentPath, 'r')
        ex = cPickle.load(loadFile)
        loadFile.close()
    else:
        ex = experiment(imgFilePath, date, strain, temp, OD, cond) #dirPath, Date, strain, temperature, startOD, condition
        ex.serialize()
    makeCropperGui(ex)
    dial.dispose()
    
def makeCropperGui(ex):
    CropperGui.ccGui(ex)


''' --- MAIN --- '''
dial = gui.initDialog(okayEvent)
