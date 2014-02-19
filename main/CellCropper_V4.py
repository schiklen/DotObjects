'''Created on Nov 19, 2013 
@author: schiklen'''

'''Importing java and ImageJ packages'''
from javax.swing import (JButton, JFrame, JPanel, JLabel, JTextField, JScrollPane, SwingConstants, WindowConstants, BoxLayout)
from java.awt import GridLayout
from os import path
from datetime import date
#from java.awt.event import KeyEvent, KeyAdapter, MouseEvent, MouseAdapter
from ij.plugin import Duplicator
from ij.plugin.frame import RoiManager
from ij.gui import Overlay, YesNoCancelDialog
from ij import IJ, WindowManager
from ij.io import OpenDialog, Opener


'''Importing own packages'''
#from containers.experiment import experiment
from containers.position import position
from containers.cell import cell


G_saveSubFold = "cutout"

def cut(event):
    roi = imp.getRoi()
    if roi != None:
        newRoi = roi.clone()
        Dup = Duplicator().run(imp, 1, imp.getNChannels(), 1, imp.getNSlices(), 1, imp.getNFrames())
        newRoi.setLocation(0,0)
        Dup.setRoi(newRoi)
        Dup.setTitle(Men.getTextField() + str(Men.getCounter()))
        Dup.show()
        #Men.setCounter()
        Men.addOlay(roi)
        imp.setOverlay(Men.getOverlay())    #setOverlay(Roi roi, java.awt.Color strokeColor, int strokeWidth, java.awt.Color fillColor) 
        imp.getOverlay().drawLabels(True) # drawNumbers
        imp.deleteRoi()
        
        #make cell instance and add to position instance
        p.addCell(cell(p.getMainPath(), p, Men.getCounter(), Dup))  #  cell(mainPath, position, ID, imp):
        Dup.close()
        Men.increaseCounter()

def delOverlay(event):
    IJ.run(imp, "Remove Overlay", "")
    print "clearOverlay"
    Men.clearOverlay()

def saveOverlay(event):
    if Men.getOverlay() != []:
        Men.saveOverlay()
        
def quit(event):    #
    Men.close()
    Men.getPosition().getImp().close()

      
class Menue(object):
    def __init__(self, p):
        self.cellCounter = 1
        self.olay = Overlay()
        self.position = p
        print p.getRoiPath()
        if p.getRoiPath() != None:         # check if there is an existing overlay file and load it!
            p.loadRois()

        self.frame = JFrame("CellCropper", size=(200,200))
        self.frame.setLocation(20,120)
        self.Panel = JPanel(GridLayout(0,1))
        self.frame.add(self.Panel)
        #self.nameField = JTextField("p" + "_c",15)
        self.nameField = JTextField("p" + str(self.position.getID()) + "_c",15)
        self.Panel.add(self.nameField)
        self.cutoutButton = JButton("Cut out cell",actionPerformed=cut)
        self.Panel.add(self.cutoutButton)
        self.delOlButton = JButton("Delete Overlay",actionPerformed=delOverlay)
        self.Panel.add(self.delOlButton)
        self.saveOlButton = JButton("Save Overlay",actionPerformed=saveOverlay)
        self.Panel.add(self.saveOlButton) 
        self.quitButton = JButton("Quit script",actionPerformed=quit)
        self.Panel.add(self.quitButton)
        self.frame.pack()
        WindowManager.addWindow(self.frame)
        self.show()
        #IJ.setTool("freehand")

    '''def getPosition(self, path, filename):
       moved to containers.position.determineID(path, filename)'''

    def eventtest(self, event):
        print "eventtest"

    def setTextField(self, pos):
        name = "p" + str(pos) + "_c"
        self.nameField.setText(name)

    def openOl(self, path, fileName):
        print "aaaaah"

    def show(self):
        self.frame.visible = True

    def close(self):
        if self.olay != None:
            yncd = YesNoCancelDialog(self.frame, "Save overlay?", "Save overlay?") #frame, title, message
            if yncd.yesPressed():
                self.saveOverlay()
        WindowManager.removeWindow(self.frame)
        self.frame.dispose()
        
    def resetCounter(self):
        self.cellCounter = 0
        
    def increaseCounter(self):
        self.cellCounter += 1
        
    def setCounter(self):
        self.cellCounter += 1
        
    #'get' functions
    def getImp(self):
        return self.imp
    
    def getCounter(self):
        return self.cellCounter
        
    def getFrame(self):
        return self.frame
        
    def getFilePath(self):
        return self.filePath

    def getTextField(self):
        return self.nameField.text
    
    def getPosition(self):
        return self.position
    
    # overlay functions
    def addOlay(self, roi):
        self.olay.add(roi)

    def getOverlay(self):
        return self.olay

    def clearOverlay(self):
        self.olay.clear()
        self.cellCounter = 1

    def saveOverlay(self):
        self.position.saveRois()   

class positionDialog(JFrame):
    def __init__(self):
        self.frame = JFrame("CellCropper: Experiment details", size=(400,200))
        self.frame.setLocation(20,120)
        self.Panel = JPanel(GridLayout(4,2))
        self.frame.add(self.Panel)
        self.Panel.add(JLabel("Date:"))
        self.dateField = JTextField( str(date.today()), 8 )
        self.Panel.add(self.dateField)
        self.strainField = JTextField( "2926",4 )
        self.Panel.add(self.strainField)
        self.tempField = JTextField( "34",2 )
        self.Panel.add(self.tempField)
        self.ODField = JTextField( "0.5",3 )
        self.Panel.add(self.ODField)
        self.condField = JTextField( "0.5",3 )
        self.Panel.add(self.condField)

        self.OKButton = JButton("OK",actionPerformed=closeAndMakePos)
        self.Panel.add(self.OKButton)
        self.frame.pack()
        WindowManager.addWindow(self.frame)
        self.show()

    def show(self):
        self.frame.visible = True
    
    def close(self):
        return self.dateField.text, self.strainField.text, self.tempField.text, self.ODField.text, self.condField.text
        WindowManager.removeWindow(self.frame)
        self.frame.dispose()

def openImp():
    '''function that calls an OpenDialog and returns filePath and imp'''
    od = OpenDialog("Open movie", "")
    filePath = path.join(od.getDirectory(), od.getFileName())
    if path.splitext(od.getFileName())[1] == ".tif" :  #on .dv, use LOCI
        imp = Opener().openImage(filePath)
    if path.splitext(od.getFileName())[1] == ".dv":
        IJ.run("Bio-Formats Importer", "open=["+filePath+"] autoscale color_mode=Grayscale view=Hyperstack stack_order=XYCZT")
        imp = IJ.getImage()
    return filePath, imp
    

def closeAndMakePos(event):
    p = position(filePath, imp) # position
    Men = Menue(p)

#--- MAIN ---
filePath, imp = openImp()
a = positionDialog()



