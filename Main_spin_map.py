# encoding: utf-8
from __future__ import division
import os, sys
sys.path.append(os.path.abspath('C:\\DATA\\Ratatouille\\Ratatouille32CD12f6'))
# sys.path.append(os.path.abspath('/Users/pierre-andremortemousque/Documents/Research/2014-15_Neel/Experimental/Ratatouille/Ratatouille32CD12f3'))
from stab12_1217_SequenceDict import Generate_SequenceInfo
import numpy as np
from libs.SionAWG_class import SionAWG
from libs.miscellanii import Normalize_mdsequence
from libs.miscellanii import Build_WFs_from_SequenceInfo
from libs.miscellanii import Build_WFs_from_SequenceInfo_Pre

def OneGateSpinMap(
        SweepChannel = 1,\
        AmplitudeStart = 0.15, \
        AmplitudeStop = 0.95,\
        NumberPoints = 80,\
        PulseDuration = 50, \
        PulsePosition = 1000,\
        WaveformDuration = 2000):

    """
    Returns NumberPoints pulses (PulseDuration,PulsePosition) on the gate
    SweepChannel with an amplitude varying from AmplitudeStart to
    AmplitudeStop.
    """

    norm = max(np.abs(AmplitudeStop),np.abs(AmplitudeStart))
    pulse_amplitudes = np.linspace(AmplitudeStart, AmplitudeStop, NumberPoints) / norm

    # Init the sequence
    sequence = {}
    sequence['WaitingSequenceElement'] = {}
    sequence['SequenceElements'] = {}
    sequence['Channels'] = {}
    sequence['NumberOfElements'] = NumberPoints

    # Build WaitingSequenceElement
    wait = {}
    wait['Name'] = 'Wait'
    wait['Size'] = WaveformDuration
    wait['Waveform'] = np.zeros((WaveformDuration,1))
    wait['Marker_1'] = []
    wait['Marker_2'] = []
    sequence['WaitingSequenceElement'] = wait

    # Build SequenceElements
    for i, pulse_amp in enumerate(pulse_amplitudes):
        i = i+1
        sequence['SequenceElements'][i] = {}
        sequence['SequenceElements'][i]['Index'] = i
        sequence['SequenceElements'][i]['Channels'] = {}
        for channel in range(1,5):
            if channel == SweepChannel:
                sequence['SequenceElements'][i]['Channels'][channel] = {}
                sequence['SequenceElements'][i]['Channels'][channel]['Name'] = 'C'+str(channel)+'P'+str(i)
                sequence['SequenceElements'][i]['Channels'][channel]['Size'] = WaveformDuration
                sequence['SequenceElements'][i]['Channels'][channel]['Waveform'] = np.zeros((WaveformDuration,1))
                sequence['SequenceElements'][i]['Channels'][channel]['Marker_1'] = []
                sequence['SequenceElements'][i]['Channels'][channel]['Marker_2'] = []
                sequence['SequenceElements'][i]['Channels'][channel]['Waveform'][PulsePosition:PulsePosition+PulseDuration]=pulse_amp
            else:
                sequence['SequenceElements'][i]['Channels'][channel] = wait

    # Set the Amplitude, Offset, Delay, Output of sequence['Channels']
    for channel in range(1,5):
        sequence['Channels'][channel] = {}
        sequence['Channels'][channel]['Offset'] = 0.0
        sequence['Channels'][channel]['Delay'] = 0.0
        sequence['Channels'][channel]['Output'] = False
        if channel == SweepChannel:
            amplitude = 2 * max(np.abs(AmplitudeStop), np.abs(AmplitudeStart))
            sequence['Channels'][channel]['Amplitude'] = max(amplitude,0.02)
        else:
            sequence['Channels'][channel]['Amplitude'] = 0.02

    return sequence

def FourGatesSequence(SequenceInfo):
    '''
    Based on the scheme: Wait until event. Then do 1 sequence. Loop
    SequenceInfo = dict:
        - 'Dimensions' = [n_i, n_j, ...]
        - 'WaitDuration' = waiting element duration
        - 'Elements' = dict:
            - i = dict:
                - Vg1 = np.array([]) @ current index
                - Vg2 = np.array([]) @ current index
                - Vg3 = np.array([]) @ current index
                - Vg4 = np.array([]) @ current index
                - Duration
                - connection to next point = 'flat'(default), 'linear ramp'
    '''

    # Determine the number of element in the sequence
    SequenceLength = np.prod(np.array(SequenceInfo['Dimensions'])) # How many different waveforms (except waits)

    # Init the sequence
    sequence = {}
    sequence['WaitingSequenceElement'] = {}
    sequence['SequenceElements'] = {}
    sequence['Channels'] = {}
    sequence['Sequence'] = {}
    sequence['SequenceLength'] = SequenceLength
    sequence['NumberOfElements'] = 0 #To be filled later

    # Build WaitingSequenceElement
    wait = {}
    wait['Name'] = 'Wait'
    wait['Size'] = SequenceInfo['WaitDuration']
    wait['Waveform'] = np.zeros((SequenceInfo['WaitDuration'],1))
    wait['Marker_1'] = []
    wait['Marker_2'] = []
    sequence['WaitingSequenceElement'] = wait

    # Build SequenceElements (only distinct wfs)
    # Build Sequence (l * n * m * ... dimensions, only wf names)
    sequence['SequenceElements'], sequence['Sequence'] = Build_WFs_from_SequenceInfo(SequenceInfo)
    sequence['NumberOfElements'] = len(sequence['SequenceElements'].keys())

    # Set the Amplitude, Offset, Delay, Output of sequence['Channels']
    sequence, Vpp = Normalize_mdsequence(sequence)
    for channel in range(1,5):
        sequence['Channels'][channel] = {}
        sequence['Channels'][channel]['Offset'] = 0.0
        sequence['Channels'][channel]['Delay'] = 0.0
        sequence['Channels'][channel]['Output'] = False
        sequence['Channels'][channel]['Amplitude'] = Vpp[channel-1,0]

    return sequence

def FourGatesSequence_Pre(PreSequenceInfo, SequenceInfo):
    '''
    Based on the scheme: Wait until event. Then do 1 constant sequence. 1 Scanning sequence. Loop
    SequenceInfo = dict:
        - 'Dimensions' = [n_i, n_j, ...]
        - 'WaitDuration' = waiting element duration
        - 'Elements' = dict:
            - i = dict:
                - Vg1 = np.array([]) @ current index
                - Vg2 = np.array([]) @ current index
                - Vg3 = np.array([]) @ current index
                - Vg4 = np.array([]) @ current index
                - Duration
                - connection to next point = 'flat'(default), 'linear ramp'
    '''

    # Determine the number of element in the sequence
    SequenceLength = np.prod(np.array(SequenceInfo['Dimensions'])) # How many different waveforms (except waits, pre and post sequences)

    # Init the sequence
    sequence = {}
    sequence['WaitingSequenceElement'] = {}
    sequence['SequenceElements'] = {}
    sequence['Channels'] = {}
    sequence['Sequence'] = {}
    sequence['SequenceLength'] = SequenceLength
    sequence['NumberOfElements'] = 0 #To be filled later

    # Build WaitingSequenceElement
    wait = {}
    wait['Name'] = 'Wait'
    wait['Size'] = SequenceInfo['WaitDuration']
    wait['Waveform'] = np.zeros((SequenceInfo['WaitDuration'],1))
    wait['Marker_1'] = []
    wait['Marker_2'] = []
    sequence['WaitingSequenceElement'] = wait

    # Build SequenceElements (only distinct wfs)
    # Build Sequence (l * n * m * ... dimensions, only wf names)
    sequence['PreSequenceElement'], sequence['SequenceElements'], sequence['Sequence'] = Build_WFs_from_SequenceInfo_Pre(PreSequenceInfo, SequenceInfo)
    sequence['NumberOfElements'] = len(sequence['SequenceElements'].keys())

    # Set the Amplitude, Offset, Delay, Output of sequence['Channels']
    sequence, Vpp = Normalize_mdsequence(sequence)
    for channel in range(1,5):
        sequence['Channels'][channel] = {}
        sequence['Channels'][channel]['Offset'] = 0.0
        sequence['Channels'][channel]['Delay'] = 0.0
        sequence['Channels'][channel]['Output'] = False
        sequence['Channels'][channel]['Amplitude'] = Vpp[channel-1,0]

    return sequence


if __name__ == '__main__':
    sion = SionAWG('192.168.1.117', 4000)

    #spinmap = OneGateSpinMap()

    PreSequenceInfo, SequenceInfo = Generate_SequenceInfo()
    # spinmap = FourGatesSequence(seqinf)
    spinmap = FourGatesSequence_Pre(PreSequenceInfo, SequenceInfo)
    sion.openCom()
    ##sion.SendSequenceLight(sequence = spinmap)
    sion.DeleteAllWaveforms()
    # sion.SendMultiDimensionnalSequenceLight(mdsequence = spinmap, resendstartindex = 0)
    # sion.SendMultiDimensionnalSequenceLight(mdsequence = spinmap, resendstartindex = 501)
    sion.SendMultiDimensionnalSequenceLight_Pre(mdsequence = spinmap, resendstartindex = 0)
    # sion.SendMultiDimensionnalSequenceLight_Pre(mdsequence = spinmap, resendstartindex = 501)
    sion.closeCom()
