# encoding: utf-8
import numpy as np
from string import ascii_lowercase

def Normalize_sequence(sequence):
    Vpp = np.zeros((4,1))
    # Find the maximum amplitude
    for i in sequence['SequenceElements'].keys():
        for channel in sequence['SequenceElements'][i]['Channels'].keys():
            if 2.*max(abs(sequence['SequenceElements'][i]['Channels'][channel]['Waveform'])) > Vpp[channel-1]:
                Vpp[channel-1] = 2.*max(abs(sequence['SequenceElements'][i]['Channels'][channel]['Waveform']))
    for i in range(1,5):
        Vpp[i-1] = max(Vpp[i-1],0.02)


    # Normalize the waveforms
    for i in sequence['SequenceElements'].keys():
        for channel in sequence['SequenceElements'][i]['Channels'].keys():
            sequence['SequenceElements'][i]['Channels'][channel]['Waveform'] = \
                sequence['SequenceElements'][i]['Channels'][channel]['Waveform']/(Vpp[channel-1]/2.0)

    return sequence, Vpp

def _get_waveform_duration(SequenceInfo, abc):
    # Find the waveform duration
    WaveformDuration = 0
    for P in SequenceInfo['Elements'].values():
        if P['Duration'].shape == (1,):
            WaveformDuration += int(P['Duration'][0])
        else:
            WaveformDuration += int(P['Duration'][abc])
    return WaveformDuration

def _Build_WF_from_SequenceInfo(SequenceInfo, abc, wfname):
    # Find the waveform duration
    WaveformDuration = _get_waveform_duration(SequenceInfo, abc)
    wf = np.zeros((WaveformDuration, 1))
    # build the waveform
    i = 0
    di = 0
    for key in SequenceInfo['Elements'].keys():
        i += di
        P = SequenceInfo['Elements'][key]
        # Determine the duration of this step
        if P['Duration'].shape == (1,):
            di = int(P['Duration'][0])
        else:
            di = int(P['Duration'][abc])

        #print abc, channel, P[channel], P[channel].shape
        # Determine the relevant voltage
        if P[channel].shape == (1,):
            v = P[channel][0]
        else:
            v = P[channel][abc]

        # Determine the voltage behavior
        if P['ToNext'] == 'flat':
            wf[i:i+di,:] = np.ones((di,1)) * v
        elif P['ToNext'] == 'ramp':
            # Determine v_next
            P_next = SequenceInfo['Elements'][key + 1]
            if P_next[channel].shape == (1,):
                v_next = P_next[channel][0]
            else:
                v_next = P_next[channel][abc]
            wf[i:i+di,:] = np.linspace(v, v_next, di)

    # return things
    return {\
        'Name':wfname, \
        'Size': WaveformDuration,\
        'Waveform': wf, \
        'Marker_1':[], \
        'Marker_2':[]}

def _update_pulse_dimensions(new_stuff, pulse_dimensions):
    # checks all elements of the list pulse_dimensions.
    # If the corresponding elements of new stuff is larger, replace
    # obvisouly, those things have to have the same shape
    new_pulse_dimensions = [0 for i in pulse_dimensions]
    for i,(new,old) in enumerate(zip(new_stuff, pulse_dimensions)):
        if new > old:
            new_pulse_dimensions[i] = new
        else:
            new_pulse_dimensions[i] = old
    return new_pulse_dimensions

def Build_WFs_from_SequenceInfo(SequenceInfo, abc, channel):
    # Init SequenceElements, Sequence
    Sequence = {}
    SequenceLength = np.prod(np.array(SequenceInfo['Dimensions'])) # How many different waveforms (except waits)
    for i in np.arange(SequenceLength):
        Sequence[i] = {'Index':i, 'Channels':{1:'', 2:'', 3:'', 3:''}}
    SequenceElements = {}

    # Loop over all Channels
    for channel in range(1,5):
        # Check if at least one parameters is stepped
        BOOL_ConstantPulse = True
        for P in SequenceInfo['Elements'].values():
            # Constant pulse
            if (P[channel].shape == (1,)) and (P['Duration'].shape == (1,)):
                BOOL_ConstantPulse = True
            else:
                BOOL_ConstantPulse = False

        if BOOL_ConstantPulse:
            # Define Constant pulse in SequenceElements
            wfname = 'C'+str(channel)
            position = tuple([0 for i in SequenceInfo['Dimensions']])
            SequenceElements[wfname] = _Build_WF_from_SequenceInfo(SequenceInfo, position, wfname)

            # Fill up Sequence
            for seqi in Sequence.values():
                seqi['Channels'][channel] = wfname

        else:
            # Multidimensionnal pulse
            # Check what are the dimensions stepped
            pulse_dimensions = [0 for i in SequenceInfo['Dimensions']]
            for P in SequenceInfo['Elements'].values():
                pulse_dimensions = _update_pulse_dimensions(P[channel].shape, pulse_dimensions)
                pulse_dimensions = _update_pulse_dimensions(P['Duration'].shape, pulse_dimensions)

            # Define pulses in SequenceElements
            # array_of_indexes,
            # indexes = flatten(array_of_indexes)
            n_pulses = np.prod(pulse_dimensions)
            for i in np.arange(n_pulses):
                index = np.unravel_index(i, pulse_dimensions)
                wfname = 'C'+str(channel)
                for j, d in enumerate(index):
                    wfname = wfname + ascii_lowercase[j] + str(d)
                SequenceElements[wfname] = _Build_WF_from_SequenceInfo(SequenceInfo, position, wfname)

            # Fill up Sequence
            for i in np.arange(SequenceLength):
                index = np.unravel_index(i, SequenceInfo['Dimensions'])
                wfname = 'C'+str(channel)
                for j, (pulse_i, seq_i) in enumerate(zip(pulse_dimensions, index)):
                    if seq_i > pulse_i - 1:
                        wfname = wfname + ascii_lowercase[j] + str(pulse_i-1)
                    else:
                        wfname = wfname + ascii_lowercase[j] + str(seq_i)
                Sequence[i][channel] = wfname
    # return things
    return SequenceElements, Sequence
