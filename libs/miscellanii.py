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

def Normalize_mdsequence(sequence):
    "Should accept pre and post sequence"

    Vpp = np.zeros((4,1))
    # Find the maximum amplitude for the Sequence
    for i in sequence['Sequence'].keys():
        for channel in sequence['Sequence'][i]['Channels'].keys():
            wfname = sequence['Sequence'][i]['Channels'][channel]
            if 2.*max(abs(sequence['SequenceElements'][wfname]['Waveform'])) > Vpp[channel-1]:
                Vpp[channel-1] = 2.*max(abs(sequence['SequenceElements'][wfname]['Waveform']))
    for i in range(1,5):
        Vpp[i-1] = max(Vpp[i-1],0.02)

    if 'PreSequenceElement' in sequence.keys():
        # Find the maximum amplitude for the PreSequence
        VppPre = np.zeros((4,1))
        for channel in sequence['PreSequenceElement'].keys():
            VppPre[channel-1] = 2.*max(abs(sequence['PreSequenceElement'][channel]['Waveform']))
        for i in range(1,5):
            Vpp[i-1] = max(VppPre[i-1], Vpp[i-1])

    if 'PostSequenceElement' in sequence.keys():
        # Find the maximum amplitude for the PreSequence
        VppPost = np.zeros((4,1))
        for channel in sequence['PostSequenceElement'].keys():
            VppPost[channel-1] = 2.*max(abs(sequence['PostSequenceElement'][channel]['Waveform']))
        for i in range(1,5):
            Vpp[i-1] = max(VppPost[i-1], Vpp[i-1])


    # Normalize the waveforms
    for wfname in sequence['SequenceElements'].keys():
        channel = sequence['SequenceElements'][wfname]['Channel']
        sequence['SequenceElements'][wfname]['Waveform'] = sequence['SequenceElements'][wfname]['Waveform']/(Vpp[channel-1]/2.0)
    for i in range(1,5):
        if 'PreSequenceElement' in sequence.keys():
            sequence['PreSequenceElement'][i]['Waveform'] = sequence['PreSequenceElement'][i]['Waveform']/(Vpp[channel-1]/2.0)
        if 'PostSequenceElement' in sequence.keys():
            sequence['PostSequenceElement'][i]['Waveform'] = sequence['PostSequenceElement'][i]['Waveform']/(Vpp[channel-1]/2.0)

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

def _Build_WF_from_SequenceInfo(SequenceInfo, abc, channel, wfname):
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
            wf[i:i+di,:] = np.reshape(np.linspace(v, v_next, di), (di,1))

    # return things
    return {\
        'Name':wfname, \
        'Size': WaveformDuration,\
        'Channel':channel,\
        'Waveform': wf, \
        'Marker_1':[], \
        'Marker_2':[]}

def _update_pulse_dimensions(new_stuff, pulse_dimensions):
    # checks all elements of the list pulse_dimensions.
    # If the corresponding elements of new stuff is larger, replace
    # obvisouly, those things have to have the same shape
    #new_pulse_dimensions = [1 for i in pulse_dimensions]
    for i, (new,old) in enumerate(zip(new_stuff, pulse_dimensions)):
        if new > old:
            pulse_dimensions[i] = new
        else:
            pulse_dimensions[i] = old
    return pulse_dimensions

def Build_WFs_from_SequenceInfo(SequenceInfo):
    # Init SequenceElements, Sequence
    Sequence = {}
    SequenceLength = np.prod(np.array(SequenceInfo['Dimensions'])) # How many different waveforms (except waits)
    for i in np.arange(SequenceLength):
        i += 1 #From numpy numbering to AWG
        Sequence[i] = {'Index':i, 'Channels':{1:'', 2:'', 3:'', 3:''}}
    SequenceElements = {}

    # Loop over all Channels
    for channel in range(1,5):
        # Check if at least one parameters is stepped
        BOOL_ConstantPulse = True
        for P in SequenceInfo['Elements'].values():
            # Constant pulse
            if (P[channel].shape == (1,)) and (P['Duration'].shape == (1,)):
                BOOL_ConstantPulse = BOOL_ConstantPulse and True
            else:
                BOOL_ConstantPulse = BOOL_ConstantPulse and False

        if BOOL_ConstantPulse:
            # Define Constant pulse in SequenceElements
            wfname = 'C'+str(channel)
            index = tuple([0 for i in SequenceInfo['Dimensions']])
            SequenceElements[wfname] = _Build_WF_from_SequenceInfo(SequenceInfo, index, channel, wfname)

            # Fill up Sequence
            for seqi in Sequence.values():
                seqi['Channels'][channel] = wfname

        else:
            # Multidimensionnal pulse
            # Check what are the dimensions stepped
            pulse_dimensions = [1 for i in SequenceInfo['Dimensions']]
            for P in SequenceInfo['Elements'].values():
                pulse_dimensions = _update_pulse_dimensions(P[channel].shape, pulse_dimensions)
                pulse_dimensions = _update_pulse_dimensions(P['Duration'].shape, pulse_dimensions)

            # Define pulses in SequenceElements
            n_pulses = np.prod(pulse_dimensions)
            for i in np.arange(n_pulses):
                index = np.unravel_index(i, pulse_dimensions)
                wfname = 'C'+str(channel)
                for j, (d, pulse_dim_j) in enumerate(zip(index, pulse_dimensions)):
                    if pulse_dim_j > 1:
                        wfname = wfname + ascii_lowercase[j] + str(d)
                SequenceElements[wfname] = _Build_WF_from_SequenceInfo(SequenceInfo, index, channel, wfname)

            # Fill up Sequence
            for i in np.arange(SequenceLength):
                index = np.unravel_index(i, SequenceInfo['Dimensions'])
                i += 1 #Python to AWG
                wfname = 'C'+str(channel)
                for j, (d, pulse_dim_j) in enumerate(zip(index, pulse_dimensions)):
                    if pulse_dim_j > 1:
                        wfname = wfname + ascii_lowercase[j] + str(d)
                Sequence[i]['Channels'][channel] = wfname

    # return things
    return SequenceElements, Sequence

def Build_WFs_from_SequenceInfo_Pre(PreSequenceInfo, SequenceInfo):
    # Init SequenceElements, Sequence
    Sequence = {}
    SequenceLength = np.prod(np.array(SequenceInfo['Dimensions'])) # How many different waveforms (except waits)
    for i in np.arange(SequenceLength):
        i += 1 #From numpy numbering to AWG
        Sequence[i] = {'Index':i, 'Channels':{1:'', 2:'', 3:'', 3:''}}
    PreSequenceElement = {1:'', 2:'', 3:'', 3:''}
    SequenceElements = {}

    ################################################################################
    # Sequence
    # Loop over all Channels
    for channel in range(1,5):
        # Check if at least one parameters is stepped
        BOOL_ConstantPulse = True
        for P in SequenceInfo['Elements'].values():
            # Constant pulse
            if (P[channel].shape == (1,)) and (P['Duration'].shape == (1,)):
                BOOL_ConstantPulse = BOOL_ConstantPulse and True
            else:
                BOOL_ConstantPulse = BOOL_ConstantPulse and False

        if BOOL_ConstantPulse:
            # Define Constant pulse in SequenceElements
            wfname = 'C'+str(channel)
            index = tuple([0 for i in SequenceInfo['Dimensions']])
            SequenceElements[wfname] = _Build_WF_from_SequenceInfo(SequenceInfo, index, channel, wfname)

            # Fill up Sequence
            for seqi in Sequence.values():
                seqi['Channels'][channel] = wfname

        else:
            # Multidimensionnal pulse
            # Check what are the dimensions stepped
            pulse_dimensions = [1 for i in SequenceInfo['Dimensions']]
            for P in SequenceInfo['Elements'].values():
                pulse_dimensions = _update_pulse_dimensions(P[channel].shape, pulse_dimensions)
                pulse_dimensions = _update_pulse_dimensions(P['Duration'].shape, pulse_dimensions)

            # Define pulses in SequenceElements
            n_pulses = np.prod(pulse_dimensions)
            for i in np.arange(n_pulses):
                index = np.unravel_index(i, pulse_dimensions)
                wfname = 'C'+str(channel)
                for j, (d, pulse_dim_j) in enumerate(zip(index, pulse_dimensions)):
                    if pulse_dim_j > 1:
                        wfname = wfname + ascii_lowercase[j] + str(d)
                SequenceElements[wfname] = _Build_WF_from_SequenceInfo(SequenceInfo, index, channel, wfname)

            # Fill up Sequence
            for i in np.arange(SequenceLength):
                index = np.unravel_index(i, SequenceInfo['Dimensions'])
                i += 1 #Python to AWG
                wfname = 'C'+str(channel)
                for j, (d, pulse_dim_j) in enumerate(zip(index, pulse_dimensions)):
                    if pulse_dim_j > 1:
                        wfname = wfname + ascii_lowercase[j] + str(d)
                Sequence[i]['Channels'][channel] = wfname

    ################################################################################
    # PreSequence
    for channel in range(1,5):
        # Define Constant pulse in SequenceElements
        wfname = 'C'+str(channel)+'Pre'
        index = tuple([0 for i in SequenceInfo['Dimensions']])
        PreSequenceElement[channel] = _Build_WF_from_SequenceInfo(PreSequenceInfo, index, channel, wfname)

    # return things
    return PreSequenceElement, SequenceElements, Sequence

def Build_WFs_from_SequenceInfo_PrePost(PreSequenceInfo, SequenceInfo, PostSequenceInfo):
    # Init SequenceElements, Sequence
    Sequence = {}
    SequenceLength = np.prod(np.array(SequenceInfo['Dimensions'])) # How many different waveforms (except waits)
    for i in np.arange(SequenceLength):
        i += 1 #From numpy numbering to AWG
        Sequence[i] = {'Index':i, 'Channels':{1:'', 2:'', 3:'', 3:''}}
    PreSequenceElement = {1:'', 2:'', 3:'', 3:''}
    PostSequenceElement = {1:'', 2:'', 3:'', 3:''}
    SequenceElements = {}

    ################################################################################
    # Sequence
    # Loop over all Channels
    for channel in range(1,5):
        # Check if at least one parameters is stepped
        BOOL_ConstantPulse = True
        for P in SequenceInfo['Elements'].values():
            # Constant pulse
            if (P[channel].shape == (1,)) and (P['Duration'].shape == (1,)):
                BOOL_ConstantPulse = BOOL_ConstantPulse and True
            else:
                BOOL_ConstantPulse = BOOL_ConstantPulse and False

        if BOOL_ConstantPulse:
            # Define Constant pulse in SequenceElements
            wfname = 'C'+str(channel)
            index = tuple([0 for i in SequenceInfo['Dimensions']])
            SequenceElements[wfname] = _Build_WF_from_SequenceInfo(SequenceInfo, index, channel, wfname)

            # Fill up Sequence
            for seqi in Sequence.values():
                seqi['Channels'][channel] = wfname

        else:
            # Multidimensionnal pulse
            # Check what are the dimensions stepped

            pulse_dimensions = [1 for i in SequenceInfo['Dimensions']]
            for P in SequenceInfo['Elements'].values():
                pulse_dimensions = _update_pulse_dimensions(P[channel].shape, pulse_dimensions)
                pulse_dimensions = _update_pulse_dimensions(P['Duration'].shape, pulse_dimensions)

            # Define pulses in SequenceElements
            n_pulses = np.prod(pulse_dimensions)
            for i in np.arange(n_pulses):
                index = np.unravel_index(i, pulse_dimensions)
                wfname = 'C'+str(channel)
                for j, (d, pulse_dim_j) in enumerate(zip(index, pulse_dimensions)):
                    if pulse_dim_j > 1:
                        wfname = wfname + ascii_lowercase[j] + str(d)
                SequenceElements[wfname] = _Build_WF_from_SequenceInfo(SequenceInfo, index, channel, wfname)

            # Fill up Sequence
            for i in np.arange(SequenceLength):
                index = np.unravel_index(i, SequenceInfo['Dimensions'])
                i += 1 #Python to AWG
                wfname = 'C'+str(channel)
                for j, (d, pulse_dim_j) in enumerate(zip(index, pulse_dimensions)):
                    if pulse_dim_j > 1:
                        wfname = wfname + ascii_lowercase[j] + str(d)
                Sequence[i]['Channels'][channel] = wfname

    ################################################################################
    # PreSequence
    for channel in range(1,5):
        # Define Constant pulse in SequenceElements
        wfname = 'C'+str(channel)+'Pre'
        index = tuple([0 for i in SequenceInfo['Dimensions']])
        PreSequenceElement[channel] = _Build_WF_from_SequenceInfo(PreSequenceInfo, index, channel, wfname)

    ################################################################################
    # PostSequence
    for channel in range(1,5):
        # Define Constant pulse in SequenceElements
        wfname = 'C'+str(channel)+'Post'
        index = tuple([0 for i in SequenceInfo['Dimensions']])
        PostSequenceElement[channel] = _Build_WF_from_SequenceInfo(PostSequenceInfo, index, channel, wfname)

    # return things
    return PreSequenceElement, SequenceElements, PostSequenceElement, Sequence
