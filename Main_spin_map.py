from __future__ import division
import numpy as np
from libs.SionAWG_class import SionAWG


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

if __name__ == '__main__':
    sion = SionAWG('192.168.1.117', 4000)

    spinmap = OneGateSpinMap()
    sion.openCom()
    sion.DeleteAllWaveforms()
    sion.SendSequenceLight(sequence = spinmap)
    sion.closeCom()
