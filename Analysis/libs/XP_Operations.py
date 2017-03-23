import numpy as np

def FFT(XP, dim):
    pass

def derivative(XP, dim, order):
    XP.ExperimentalData['data'] = np.diff(XP.ExperimentalData['data'], n = order, axis = dim)

def FFTfilter(XP, fftfilters, dim):
    pass

def smooth(XP, smooth_type, dim):
    sh = XP.ExperimentalData['data'].shape
    print sh

def average(XP, dim):
    pass
