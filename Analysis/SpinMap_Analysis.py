from __future__ import division
import h5py
import numpy as np
import libs.MultiDimExperiment as MultiDimExperiment
import libs.ExperimentFileManager as ExperimentFileManager
import matplotlib.pyplot as plt

XP = MultiDimExperiment.MultiDimExperiment()
FM = ExperimentFileManager.ExperimentFileManager(XP)
filepath = '/Users/pierre-andremortemousque/Documents/Research/2014-15_Neel/Experimental/Ratatouille/Ratatouille32CD12f0'
filename = 'stab11_488'
ExperimentType = 'SpinMap'

"""
QPCs = BL
"""

# Read lvm file and convert to h5
# Group = raw_data
if True:
    FM.Read_Experiment_File(\
        filepath = filepath,\
        filename = filename + '.lvm',\
        read_multiple_files = True)

    XP.WSPversion = 1.0
    XP.WSPPython = True
    XP.ExperimentType = ExperimentType

    FM.Write_Experiment_to_h5(\
        filename = filename + '.h5',\
        group_name = 'raw_data',\
        force_overwrite = True)

# Read binary raw_data and compute derivative for the measurement
# Group = TunnelOutMeas
if True:
    FM.Read_Experiment_File(\
        filepath = filepath,\
        filename = filename + '.h5',\
        group_name = 'raw_data')

    # init, BL loaded, TR loaded, TL loaded, BL unloaded, TR unloaded, TL unloaded
    region = [91,200]

    final_shape = XP.ExperimentalData['dimensions']
    final_shape[1] = region[1]-region[0]
    locdata = np.zeros(final_shape)

    locdata[:,:,:,:,:] = np.gradient(\
        XP.ExperimentalData['data'][:,region[0]:region[1],:,:,:], \
        axis = 1)

    XP.ExperimentalData['dimensions'][1] = final_shape[1]
    XP.ExperimentalData['data'] = locdata

    FM.Write_Experiment_to_h5(group_name = 'TunnelOutMeas')


# Plot derivative histogram
if False:
    FM.Read_Experiment_File(\
        filepath = filepath,\
        filename = filename + '.h5',\
        group_name = 'TunnelOutMeas')

    lim_inf = 00
    lim_sup = 100
    nbins = 3000

    fig = plt.figure()

    data = XP.ExperimentalData['data'][0, :, :, :, 0]
    data = data.flatten()

    n, bins, patches = plt.hist(data, nbins, facecolor='blue', alpha = 0.75)
    plt.xlabel('Derivative of the current BL (a.u.)')
    plt.ylabel('Counts BL')
    plt.grid(True)

    plt.show()



# Plot 2d spin map
if False:
    FM.Read_Experiment_File(\
        filepath = filepath,\
        filename = filename + '.h5',\
        group_name = 'TunnelOutMeas')

    # print XP.ExperimentalParameters.keys()
    #timings = XP.ExperimentalParameters['moving_parameters']['timing [43]']['values']
    #timings = timings.flatten()

    locdim = XP.ExperimentalData['dimensions']
    thres = 0.00033
    index_min = 2
    index_max = locdim[1]
    counts = np.zeros((locdim[2],locdim[3]))


    for i in range(locdim[4]): # Over all repetitions
        for j in range(locdim[3]):
            for k in range(locdim[2]): # all timings
                if np.any(XP.ExperimentalData['data'][0, index_min:index_max, k, j, i]>thres):
                    counts[k,j] += 1
    counts = counts / locdim[4]

    fig = plt.figure()

    #plt.plot(timings, counts, alpha = 0.75)
    plt.imshow(counts)
    plt.xlabel('Axis 1')
    plt.ylabel('Axis 2')
    plt.grid(True)

    plt.show()
