'''
Created on Feb 3, 2014

@author: schiklen
'''

import ij.IJ
from de.embl.cmci import FFTFilter_NoGenDia
imp = IJ.openImage("http://imagej.nih.gov/ij/images/blobs.gif")
test = FFTFilter_NoGenDia()
test.core(imp)
imp.show()