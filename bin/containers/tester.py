import thread
from javax.swing import JList, JFrame, JButton, JPanel, DefaultListModel, JScrollPane
from java.awt import GridLayout
#from containers.experiment import experiment
#from containers.position import position
#from containers.cell import cell
#from containers.frame import frame
#from containers import CONSTANTS
from os import path, makedirs
import gui, CropperGui


#makedirs('/Users/schiklen/testest')

def rem(event):
    if li.getSelectedIndex() >=0:
        listModel.remove(li.getSelectedIndex())

def click(event):
    print li.getSelectedIndex()

def add(event):
    listModel.addElement("7")

def change(event):
    listModel.clear()
    [listModel.addElement(e) for e in b]

liste = [1,2,3,4]
b = [6,8,9]
f = JFrame("list")
frame2 = JFrame("frame2")

f.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE)


p = JPanel()
grid = GridLayout(3,1)
p.setLayout(grid)

button = JButton("selected?", actionPerformed=click)
addButton = JButton("add 7", actionPerformed=add)
remButton = JButton("remove element", actionPerformed=rem)
chButton = JButton("Change to list B", actionPerformed=change)



listModel = DefaultListModel()
[listModel.addElement(e) for e in liste]
li = JList(listModel)
spane = JScrollPane(li) # making the list scrollable. li is now inside container JScrollPane


#b = JButton("press", actionPerformed=rem)
p.add(spane)
p.add(button)
p.add(addButton)
p.add(remButton)
p.add(chButton)
f.add(p)
f.pack()
f.setLocationRelativeTo(None)
f.setVisible(True)

print f.getParent()
print f.getLocationOnScreen()
print f.getContentPane().getSize()


