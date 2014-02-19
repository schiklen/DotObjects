'''
Created on Dec 10, 2013

@author: schiklen
'''
#!/usr/local/bin/jython
# -*- coding: utf-8 -*-

"""
ZetCode Jython Swing tutorial

In this program, use box layouts
to position two buttons in the
bottom right corner of the window

author: Jan Bodnar
website: www.zetcode.com
last modified: November 2010
"""

from java.awt import Dimension
from javax.swing import JButton, JLabel, JFrame, JPanel, GroupLayout, JTextField, LayoutStyle
from java.lang.System import exit
from ij.io import OpenDialog
#from os.datetime import date

def cancel(event):
    exit(0)


class Example(JFrame):

    def __init__(self):
        super(Example, self).__init__()

        self.initUI()

    def initUI(self):
        #panel = 
        layout = GroupLayout(self.getContentPane())
        self.getContentPane().setLayout(layout)
        layout.setAutoCreateGaps(True)
        layout.setAutoCreateContainerGaps(True)
        #self.setPreferredSize(Dimension(300, 300))
        self.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE)
        # definition of elements
        # labels
        dateLabel = JLabel("Date:")
        strainLabel = JLabel("Strain:")
        tempLabel = JLabel("Temperature:")
        dCelLabel = JLabel("C")
        ODLabel = JLabel("OD:")
        condLabel = JLabel("Condition:")
        
        #textfields
        dateField = JTextField( "today", 1)#str(date.today()), 8 )
        strainField = JTextField( "2926",1 )
        tempField = JTextField( "34",2 )
        ODField = JTextField( "0.5",3 )
        condField = JTextField( "0.5",3 )
        
        #buttons
        OKButton = JButton("OK",actionPerformed=None)
        CancelButton = JButton("Cancel", actionPerformed=cancel)
        
        '''horizontal layout = parallel group (sequential group (c1, c2), sequential group(c3,c4))
           vertical layout = parallel group ( sequential group(c1,c3), sequential group(c2,c4))'''
        
        layout.setHorizontalGroup(layout.createSequentialGroup()
                                  .addGroup(layout.createParallelGroup()
                                            .addComponent(dateLabel)
                                            .addComponent(strainLabel)
                                            .addComponent(tempLabel)
                                            .addComponent(ODLabel)
                                            .addComponent(condLabel))
                                  .addGroup(layout.createParallelGroup()
                                            .addComponent(dateField)
                                            .addComponent(strainField)
                                            .addGroup(layout.createSequentialGroup()
                                                      .addComponent(tempField)
                                                      .addComponent(dCelLabel))
                                            .addComponent(ODField)
                                            .addComponent(condField)
                                            .addGroup(layout.createSequentialGroup()
                                                      .addComponent(CancelButton)
                                                      .addComponent(OKButton)
                                                      .addPreferredGap(LayoutStyle.ComponentPlacement.RELATED)
                                                      )
                                            )
                                  )
        layout.setVerticalGroup(layout.createSequentialGroup()
                                .addGroup(layout.createParallelGroup(GroupLayout.Alignment.BASELINE)
                                          .addComponent(dateLabel)
                                          .addComponent(dateField)
                                          )
                                .addGroup(layout.createParallelGroup(GroupLayout.Alignment.BASELINE)
                                          .addComponent(strainLabel)
                                          .addComponent(strainField)
                                          )
                                .addGroup(layout.createParallelGroup(GroupLayout.Alignment.BASELINE)
                                          .addComponent(tempLabel)
                                          .addComponent(tempField)
                                          .addComponent(dCelLabel)
                                          )                                
                                .addGroup(layout.createParallelGroup(GroupLayout.Alignment.BASELINE)
                                          .addComponent(ODLabel)
                                          .addComponent(ODField)
                                          )                                      
                                .addGroup(layout.createParallelGroup(GroupLayout.Alignment.BASELINE)
                                          .addComponent(condLabel)
                                          .addComponent(condField)
                                          )
                                .addGroup(layout.createParallelGroup(GroupLayout.Alignment.BASELINE)
                                          .addComponent(CancelButton)
                                          .addComponent(OKButton))    
                              )
    
        

        self.setTitle("CellSelector")

        #self.setSize(200, 150)
        self.pack()
        self.setLocationRelativeTo(None)
        self.setVisible(True)


if __name__ == '__main__':
    Example()