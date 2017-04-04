# encoding: utf-8
import numpy as np

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


def Build_WF_from_SequenceInfo(SequenceInfo, abc, channel):
    # Find the waveform duration
    WaveformDuration = 0
    for P in SequenceInfo['Elements'].values():
        if P['Duration'].shape == (1,):
            WaveformDuration += int(P['Duration'][0])
        else:
            WaveformDuration += int(P['Duration'][abc])

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
    return WaveformDuration, wf
