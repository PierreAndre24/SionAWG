import string, re, os, h5py
import numpy as np

class h5_IO:


    def __init__(self, read_fstsq = True):
        pass

    def Read_data(self, filepath, filename, XP, group_name, read_multiple_files = False):
        with h5py.File(filepath + os.sep + filename,'r') as f:
            XP.ExperimentalData['data'] = f.get(group_name + '/ExperimentalData')[:]

            for k in f[group_name]['ExperimentalData'].attrs.keys():
                XP.ExperimentalData[k] = f[group_name]['ExperimentalData'].attrs[k]

            moving_parameters = f[group_name]['ExperimentalParameters'].attrs['all_moving_parameters']
            XP.ExperimentalParameters['moving_parameters'] = {}
            for mp in moving_parameters:
                XP.ExperimentalParameters['moving_parameters'][mp] = {}
                XP.ExperimentalParameters['moving_parameters'][mp]['values'] = f.get(group_name + '/ExperimentalParameters/' + mp)[:]
                XP.ExperimentalParameters['moving_parameters'][mp]['dimensions'] = f[group_name]['ExperimentalParameters'][mp].attrs['dimensions']
                XP.ExperimentalParameters['moving_parameters'][mp]['unit'] = f[group_name]['ExperimentalParameters'][mp].attrs['unit']
                XP.ExperimentalParameters['moving_parameters'][mp]['param_type'] = f[group_name]['ExperimentalParameters'][mp].attrs['param_type']
                if 'DAC' in XP.ExperimentalParameters['moving_parameters'][mp]['param_type']:
                    XP.ExperimentalParameters['moving_parameters'][mp]['DAC_row'] = f[group_name]['ExperimentalParameters'][mp].attrs['DAC_row']
                    XP.ExperimentalParameters['moving_parameters'][mp]['DAC_column'] = f[group_name]['ExperimentalParameters'][mp].attrs['DAC_column']
                if 'fast' in XP.ExperimentalParameters['moving_parameters'][mp]['param_type']:
                    XP.ExperimentalParameters['moving_parameters'][mp]['slot'] = f[group_name]['ExperimentalParameters'][mp].attrs['slot']

    def Read_FastSequence(self, filepath, filename, XP, group_name):
        XP.ExperimentalParameters['Info']['Fastchannels'] = {}
        with h5py.File(filepath + os.sep + filename,'r') as f:
            XP.ExperimentalParameters['Fastsequence'] = f.get(group_name + '/ExperimentalParameters/Fastsequence')[:]
            for k in f[group_name]['ExperimentalParameters']['Fastsequence'].attrs.keys():
                if k != 'Fastchannels':
                    XP.ExperimentalParameters['Info'][k] = f[group_name]['ExperimentalParameters']['Fastsequence'].attrs[k]
                else:
                    Fastchannels = f[group_name]['ExperimentalParameters']['Fastsequence'].attrs['Fastchannels']
                    Fastchannels = list(Fastchannels)
                    Fastchannels = [list(x) for x in Fastchannels]
                    #Fastchannels = Fastchannels.reshape(Fastchannels.shape[1],Fastchannels.shape[0])
                    for index, DAC_column, DAC_row in Fastchannels:
                        XP.ExperimentalParameters['Info']['Fastchannels'][index] = [DAC_column,DAC_row]

    def Read_header(self, filepath, filename, XP, group_name):
        with h5py.File(filepath + os.sep + filename,'r') as f:

            for k in f[group_name]['ExperimentalParameters'].attrs.keys():
                XP.ExperimentalParameters['Info'][k] = f[group_name]['ExperimentalParameters'].attrs[k]

            for k in f[group_name].attrs.keys():
                XP.FileInfo[k] = f[group_name].attrs[k]

            # XP.WSPPython = f.attrs['WSPPython']
            # XP.WSPversion = f.attrs['WSPversion']
            # XP.ExperimentType = f.attrs['ExperimentType']
