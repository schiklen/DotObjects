'''
Created on Dec 10, 2013
@author: schiklen
'''

from javax.swing import JButton, JLabel, JFrame, GroupLayout, JTextField, JPanel
from java.lang.System import exit
from ij.io import OpenDialog
from os import path
from datetime import date

class initDialog(JFrame):

    def __init__(self, okayEvent):
        super(initDialog, self).__init__()

        self.initUI(okayEvent)

    def initUI(self, okayEvent):
        pathPanel = JPanel()
        pPLayout = GroupLayout(pathPanel)
        pathPanel.setLayout(pPLayout)
        pPLayout.setAutoCreateContainerGaps(True)
        pPLayout.setAutoCreateGaps(True)

        btnPanel = JPanel()
        btnLayout = GroupLayout(btnPanel)
        btnPanel.setLayout(btnLayout)
        btnLayout.setAutoCreateContainerGaps(True)
        btnLayout.setAutoCreateGaps(True)
        
        paramPanel = JPanel()
        paramLayout = GroupLayout(paramPanel)
        paramPanel.setLayout(paramLayout)
        paramLayout.setAutoCreateContainerGaps(True)
        paramLayout.setAutoCreateGaps(True)
        
        layout = GroupLayout(self.getContentPane())
        self.getContentPane().setLayout(layout)
        layout.setAutoCreateGaps(True)
        layout.setAutoCreateContainerGaps(True)

        self.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE)
        # definition of elements
        # labels
        pathLabel = JLabel("Path:")
        dateLabel = JLabel("Date:")
        strainLabel = JLabel("Strain:")
        tempLabel = JLabel("Temperature:")
        dCelLabel = JLabel("C")
        ODLabel = JLabel("OD:")
        condLabel = JLabel("Condition:")
        
        #textfields
        self.pathField = JTextField("",1)
        self.dateField = JTextField( str(date.today()), 8 )
        self.strainField = JTextField( "2926",1 )
        self.tempField = JTextField( "34",2 )
        self.ODField = JTextField( "0.5",3 )
        self.condField = JTextField( "",3 )
        
        #buttons
        OpenPathButton = JButton("Browse...", actionPerformed=self.browse)
        OKButton = JButton("OK",actionPerformed=okayEvent)
        CancelButton = JButton("Cancel", actionPerformed=self.cancel)
        
        '''ContentPane Layout'''
        layout.setHorizontalGroup(layout.createParallelGroup()
                                  .addComponent(pathPanel)
                                  .addComponent(paramPanel)
                                  .addComponent(btnPanel)
                                  )
        layout.setVerticalGroup(layout.createSequentialGroup()
                                .addComponent(pathPanel)
                                .addComponent(paramPanel)
                                .addComponent(btnPanel)
                                )
        
        
        ''' PathChooser Panel Layout '''
        pPLayout.setHorizontalGroup(pPLayout.createSequentialGroup()
                                    .addComponent(pathLabel)
                                    .addComponent(self.pathField)
                                    .addComponent(OpenPathButton)
                                    )
        
        pPLayout.setVerticalGroup(pPLayout.createParallelGroup(GroupLayout.Alignment.BASELINE)
                                  .addComponent(pathLabel)
                                  .addComponent(self.pathField)
                                  .addComponent(OpenPathButton)
                                  )
        
        '''Param Panel Layout'''
        paramLayout.setHorizontalGroup(paramLayout.createSequentialGroup()
                                       .addGroup(paramLayout.createParallelGroup()
                                                 .addComponent(dateLabel)
                                                 .addComponent(strainLabel)
                                                 .addComponent(tempLabel)
                                                 .addComponent(ODLabel)
                                                 .addComponent(condLabel))
                                       .addGroup(paramLayout.createParallelGroup()
                                                .addComponent(self.dateField)
                                                .addComponent(self.strainField)
                                                .addGroup(paramLayout.createSequentialGroup()
                                                          .addComponent(self.tempField)
                                                          .addComponent(dCelLabel))
                                                .addComponent(self.ODField)
                                                .addComponent(self.condField)
                                                )
                                       )
        
        paramLayout.setVerticalGroup(paramLayout.createSequentialGroup()
                                .addGroup(paramLayout.createParallelGroup(GroupLayout.Alignment.BASELINE)
                                          .addComponent(dateLabel)
                                          .addComponent(self.dateField)
                                          )
                                .addGroup(paramLayout.createParallelGroup(GroupLayout.Alignment.BASELINE)
                                          .addComponent(strainLabel)
                                          .addComponent(self.strainField)
                                          )
                                .addGroup(paramLayout.createParallelGroup(GroupLayout.Alignment.BASELINE)
                                          .addComponent(tempLabel)
                                          .addComponent(self.tempField)
                                          .addComponent(dCelLabel)
                                          )                                
                                .addGroup(paramLayout.createParallelGroup(GroupLayout.Alignment.BASELINE)
                                          .addComponent(ODLabel)
                                          .addComponent(self.ODField)
                                          )                                      
                                .addGroup(paramLayout.createParallelGroup(GroupLayout.Alignment.BASELINE)
                                          .addComponent(condLabel)
                                          .addComponent(self.condField)
                                          )  
                              )
        
        '''Buttons Panel Layout'''
        btnLayout.setHorizontalGroup(btnLayout.createSequentialGroup()
                                     .addComponent(CancelButton)
                                     .addComponent(OKButton)
                                     )
        btnLayout.setVerticalGroup(btnLayout.createParallelGroup(GroupLayout.Alignment.BASELINE)
                                   .addComponent(CancelButton)
                                   .addComponent(OKButton)
                                   )

        self.setTitle("CellSelector")

        #self.setSize(200, 150)
        self.pack()
        self.setLocationRelativeTo(None)
        self.setVisible(True)
        
        self.browse(self)
        
        #if experiment is present, load!
        
    '''Event-Methods'''    
    def browse(self, event):
        od = OpenDialog("Select Position", "")
        filePath = path.join(od.getDirectory(), od.getFileName())
        self.pathField.text = filePath    
        
    def cancel(self, event):
        exit(0)
        
    def confirmValues(self, event):
        print self.pathField.text
        
    def getValues(self):
        return self.pathField.text, self.dateField.text, self.strainField.text, self.tempField.text, self.ODField.text, self.condField.text

