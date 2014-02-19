'''Created on Nov 18, 2013
@author: christoph.schiklenk@embl.de'''

from ij import IJ, gui #ImagePlus
#from java.awt import Color
from ij.plugin import Duplicator, ZProjector
from ij.gui import Overlay
from ij.io import Opener
from cell import cell
from os import path, remove #listdir
from containers import CONSTANTS as C
import re


class position(object):
    '''class position describing imaging position field of views '''

    def __init__(self, filePath, ID):
        '''Constructor'''
        self.filePath = filePath # see next line !?
        self.impPath = filePath  # fix this douplicate!!
        self.imp = None
        self.zImp = None
        self.dirPath, self.fileName = path.split(self.filePath)
        self.ID = ID
        self.cells = []
        self.cellsDir = path.join(path.split(self.dirPath)[0], C.CUTOUT_DIR)
        self.isDriftCorrected = False
        self.isDone = False

    def openImp(self):
        '''method for differential loading of DV or TIF encoded images.'''
        regex = re.compile('(?P<prefix>.+)(?P<suffix>\.tif|\.dv)$')
        if regex.match(self.impPath):  #on .dv, use LOCI
            if regex.match(self.impPath).group('suffix') == ".tif":
                self.imp = Opener().openImage(self.impPath)
            if regex.match(self.impPath).group('suffix') == ".dv":
                IJ.run("Bio-Formats Importer", "open=["+self.impPath+"] autoscale color_mode=Grayscale view=Hyperstack stack_order=XYCZT use_virtual_stack")
                self.imp = IJ.getImage()
        self.imp.show()
        if self.imp.getOverlay() == None:        # check, if tiff has overlay already, if not,
            self.imp.setOverlay( gui.Overlay() )  # create an empty one.
        #self.showZProj()
    
    def showZProj(self):    #show imp as Z-projection
        zP = ZProjector(self.imp)
        zP.doRGBProjection(True)
        self.zImp = zP.getProjection()
        self.zImp.show()
        
    def getImp(self):
        return self.imp
    
    def __getstate__(self): # set pickling options: overlay and imp not serialized!
        state = self.__dict__.copy()
        try:
            del state["imp"]
        except KeyError:
            pass
            #print "Copy of __dict__ has no self.imp"
        #del state["zImp"]
        return state
        
    def setCalibration(self, imp):
        self.pxWidth = imp.getCalibration().pixelWidth  # float pxWidth in microns
        self.timeInterval = round(imp.getCalibration().frameInterval) # int timeInterval in seconds
             
    def saveRois(self):
        print "Saving overlay"
        IJ.saveAsTiff(self.imp, self.impPath) #save .tiff and delete .dv if present.
                    
    def delRois(self):
        self.imp.getOverlay().clear()
    
    def getImpPath(self):
        return self.impPath
    
    def getID(self):
        return self.ID
        
    def addCell(self, c):
        self.cells.append(c)
    
    def getCells(self):
        return self.cells
    
    def setIsDone(self,z):
        self.isDone = z
        
    def getIsDone(self):
        return self.isDone
    
    def getMainPath(self):
        return path.split(self.dirPath)[0]

    def makeCellID(self):
        try:
            cellID = max([c.getID() for c in self.cells]) + 1 # Nicer would be: first occurrence of gap in sequence.
        except ValueError:
            cellID = 1
        return cellID
    
    '''--- All event methods for ccGui ---'''
    def defineCell(self):
        roi = self.imp.getRoi()
        if self.imp.getOverlay() == None: # in case imp has no overlay
            self.imp.setOverlay(Overlay()) # set an empty one.
            
        if roi != None and roi.isArea():
            newRoi = roi.clone()
            Dup = Duplicator().run(self.imp, 1, self.imp.getNChannels(), 1, self.imp.getNSlices(), 1, self.imp.getNFrames())
            newRoi.setLocation(0,0)
            Dup.setRoi(newRoi)
            cellID = self.makeCellID()
            dupTitle = "p" + str(self.ID) + "_c" + str(cellID)
            Dup.setTitle(dupTitle)
            Dup.show()

            c = cell(self, cellID, self.cellsDir, Dup) #Construct cell instance
            self.addCell(c) # adding cell instance to position

            # add roi of cell to imp and name it "id" of cell object that will be created.
            roi.setName(str(cellID))
            self.imp.getOverlay().add(roi)
            self.imp.deleteRoi()    # instantly remove the roi again to prevent moving.
            self.imp.setOverlay(self.imp.getOverlay()) # just to refresh the screen
            self.imp.getOverlay().drawLabels(False)
            self.imp.getOverlay().drawNames(True)
            Dup.close()


    def deleteCell(self, cellID):
        deleteCells = [cell for cell in self.cells if int(cell.getID())==cellID]   # if more than one cell is selected in the list.
        for cell in deleteCells:
            i = self.imp.getOverlay().getIndex( str(cell.getID()) )  # get the index of the ROI in overlay that has the name of the cell's ID (= the cells roi)
            self.imp.getOverlay().remove(i)
            remove(cell.getRawImageFilePath())            # remove cell's files 
            #remove(cell.getPpcdImageFilePath())
            #remove(cell.getMeasImageFilePath())
            #remove(cell.getMeasValFilePath())
            #remove(cell.getqcValFilePath())
            self.cells.remove(cell)                       # remove the cell object from the position's file list
            #clean!
        self.imp.setOverlay(self.imp.getOverlay()) # refresh the screen.

    '''def highlightCellRoi(self, i):
        #--- move this to GUI ?? ---
        #make overlay with different color.
        #1. get list of all rois from cell list
        O = Overlay()
        for c in self.cells:
            roi = c.getRoiInPosition()
            if self.cells.index(c) == i:
                roi.setColor(C.SELECTED_OVERLAY_COLOR) #here: put Color into constants!
            else:
                roi.setColor(C.OVERLAY_COLOR)
            O.add(roi)
            self.imp.setOverlay(O)'''
