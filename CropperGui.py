'''Created on Dec 12, 2013
@author: schiklen'''

from javax.swing import JFrame, JPanel, JButton, JLabel, GroupLayout, JList, DefaultListModel, JScrollPane
from javax.swing.event import ListSelectionListener
from java.awt import GridLayout, Dimension
from java.lang.System import exit
from ij import IJ
from ij.gui import Toolbar, Roi
from ij.io import Opener
from ij.plugin.frame import RoiManager
import re

class lsl(ListSelectionListener):
    def __init__(self, ex):
        self.ex = ex
    
    '''def valueChanged(self, event):
        listSelectionModel = event.getSource()
        if listSelectionModel.getValueIsAdjusting() == False:
            i = listSelectionModel.getMinSelectionIndex()
            self.ex.getCurrPos().highlightCellRoi(i)'''


class ccGui(JFrame):

    def __init__(self, ex):
        '''Load the GUI based on an experiment object.'''
        super(ccGui, self).__init__()
        self.ex = ex
        ex.getCurrPos().openImp() #
        self.initUI()
        #IJ.setTool(Roi.FREEROI)
        #IJ.setTool(3)#Toolbar.FREEROI)

    def initUI(self):
        self.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE)
        
        layout = GroupLayout(self.getContentPane()) #
        self.getContentPane().setLayout(layout) #
        layout.setAutoCreateGaps(True)
        layout.setAutoCreateContainerGaps(True)

        bPanel = JPanel()
        grid = GridLayout(7,1) # rows, cols
        bPanel.setLayout(grid)
        #bLayout.setAutoCreateContainerGaps(True)
        #bLayout.setAutoCreateGaps(True)
        
        # - Buttons -
        cutButton = JButton("Define Cell", actionPerformed=self.cutButtonLambda)
        delCellButton = JButton("Delete Cell", actionPerformed=self.deleteCell)
        #saveOLButton = JButton("Delete Cell", actionPerformed=self.saveOverlayButton)
        doneButton = JButton("Done with pos", actionPerformed = self.doneButton)
        delOLButton = JButton("Delete Overlay", actionPerformed=self.deleteOverlayButton)
        nextPosButton = JButton("Next Position ->", actionPerformed=self.openNextPos)
        prevPosButton = JButton("<- Previous Position", actionPerformed=self.openPrevPos)
        quitButton = JButton("Quit", actionPerformed=self.end)
        
        bPanel.add(cutButton)
        bPanel.add(delCellButton)
        #bPanel.add(saveOLButton)
        bPanel.add(doneButton)
        bPanel.add(delOLButton)
        bPanel.add(nextPosButton)
        bPanel.add(prevPosButton)
        bPanel.add(quitButton)
        
        # - CellList -
        self.cellListModel = DefaultListModel()
        #self.updateCellList()
        
        self.cellGuiList = JList(self.cellListModel) # JList showing all the cells, for convenient deletion of incorrectly annotated rois.
        listSelectionModel = self.cellGuiList.getSelectionModel()
        listSelectionModel.addListSelectionListener(lsl(self.ex))
        spane = JScrollPane(self.cellGuiList)
        spane.setSize(190, 160)
        
        cPgrid = GridLayout(1,1)
        cPanel = JPanel()
        cPanel.setLayout(cPgrid)
        cPanel.add(spane)
        cPanel.setSize(120, 120)

                
        # - Define Layout: -
        layout.setHorizontalGroup(layout.createParallelGroup()
                                  .addComponent(bPanel)
                                  .addComponent(cPanel)
                                  )
        layout.setVerticalGroup(layout.createSequentialGroup()
                                .addComponent(bPanel)
                                .addComponent(cPanel))
        
        self.setTitle("CellSelector")
        self.setSize(200, 400)
        # not working! self.setLocationRelativeTo(self.imp.getWindow())
        self.setVisible(True)
        self.updateCellList()
        
    def updateCellList(self):
        self.cellListModel.clear()
        [self.cellListModel.addElement(c.getID()) for c in self.ex.getCurrPos().getCells()]

    def getListModel(self):
        return self.cellListModel
    
    def end(self, event):
        # dialog asking for saving!
        self.ex.getCurrPos().saveRois()   
        self.ex.serialize()
        exit(0)

    def doneButton(self, event):
        self.ex.getCurrPos().saveRois()
        self.ex.getCurrPos().setIsDone(True)
        if self.ex.getCurrPos().getID() < len(self.ex.getPositions()):
            self.ex.getCurrPos().getImp().close()
            self.ex.incrementPos()
            self.ex.getCurrPos().openImp()
            self.updateCellList()
        self.ex.serialize()

    def openNextPos(self, event):
        self.ex.getCurrPos().saveRois()   #ask if save overlay or just do
        if self.ex.getCurrPos().getID() < len(self.ex.getPositions()):
            self.ex.getCurrPos().getImp().close()
            self.ex.incrementPos()
            self.ex.getCurrPos().openImp()
            self.updateCellList()
            self.ex.serialize()
        else:
            self.ex.serialize()
            print "Last Position, I can't go further!"
    
    def openPrevPos(self, event):
        self.ex.getCurrPos().saveRois()   #ask if save overlay or just do
        if self.ex.getCurrPos().getID() > 1:
            self.ex.getCurrPos().getImp().close()
            self.ex.decrementPos()
            self.ex.getCurrPos().openImp()
            self.updateCellList()
            self.ex.serialize()
        else:
            self.ex.serialize()
            print "First position!"
        
    def cutButtonLambda(self, event):
        '''an event function that calls the current position's defineCell function with the current imp.
        Was before: cutButton actionPerfromed=lambda x, param=self.imp: self.ex.currPos.defineCell(self, param))
        but this solution had the bug that when loading a different position, lambda was not called again and was still refencing to the old self.imp.
        lambda: call 'defineCell' function of currPos using the parameter self.imp, see http://www.javalobby.org/articles/jython/'''
        self.ex.getCurrPos().defineCell()
        self.updateCellList()
        
    def deleteCell(self, event):
        selection = self.cellGuiList.getSelectedIndex()
        ID = self.cellListModel.get(selection)
        self.ex.getCurrPos().deleteCell(ID)
        self.updateCellList()
    
    def saveOverlayButton(self, event):
        IJ.saveAs(self.imp, ".tiff", self.ex.getCurrPos().getImpPath())
    
    def deleteOverlayButton(self, event):
        self.ex.getCurrPos().getImp().getOverlay().clear() # clear overlay
        self.ex.getCurrPos().getImp().setOverlay(self.ex.getCurrPos().getImp().getOverlay())# refresh screen

        

