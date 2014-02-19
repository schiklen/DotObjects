'''
Created on Nov 18, 2013

@author: schiklen
'''
from java.awt import Color
# regular expressions and directory structure definitions

RAW_DIR = "raw"
PPCD_DIR = "ppcd"
MEAS_DIR = "meas"
QCMEAS_DIR = "qcmeas"
CUTOUT_DIR = "cutout"
DRIFTCOR_DIR = "driftcorr"
ANALYSIS_DIR = "Analysis"

PREPROCESSED_PREFIX = "ppcd_"
MEASUREDIMAGE_PREFIX = "zi_"
MEASUREMENT_RESULTS_TSV_PREFIX = "val_"
VERIFIED_RESULTS_TSV_PREFIX = "qcval_"

OVERLAY_COLOR = Color(255,255,0)
SELECTED_OVERLAY_COLOR = Color(0,255,255)