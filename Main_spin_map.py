from __future__ import division
import numpy as np
from libs.SionAWG_class import SionAWG


def OneGateSpinMap(
        SweepChannel = 1,\
        AmplitudeMin = 0, \
        AmplitudeMax = 0.1,\
        NumberPoints = 10,\
        PulseDuration = 50, \
        PulsePosition = 15000,\
        WaveformDuration = 16000):

    pulse_amplitudes = np.linspace(AmplitudeMin, AmplitudeMax, NumberPoints)

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
    wait['Waveform'] = np.zeros((1,WaveformDuration))
    wait['Marker_1'] = []
    wait['Marker_2'] = []
    sequence['WaitingSequenceElement'] = wait

    # Build SequenceElements
    for i, pulse_amp in enumerate(pulse_amplitudes):
        sequence['SequenceElements'][i] = {}
        sequence['SequenceElements'][i]['Index'] = i
        sequence['SequenceElements'][i]['Channels'] = {}
        for channel in range(1,5):
            if channel == SweepChannel:
                sequence['SequenceElements'][i]['Channels'][channel]['Name'] = 'C'+str(channel)+'P'+str(i)
                sequence['SequenceElements'][i]['Channels'][channel]['Size'] = WaveformDuration
                sequence['SequenceElements'][i]['Channels'][channel]['Waveform'] = np.zeros((1,WaveformDuration))
                sequence['SequenceElements'][i]['Channels'][channel]['Marker_1'] = []
                sequence['SequenceElements'][i]['Channels'][channel]['Marker_2'] = []
                sequence['SequenceElements'][i]['Channels'][channel]['Waveform'][PulsePosition:PulsePosition+PulseDuration]=pulse_amp
            else:
                sequence['SequenceElements'][i]['Channels'][channel] = wait
                sequence['SequenceElements'][i]['Channels'][channel]['Name'] = 'PulseC'+str(channel)
                sequence['SequenceElements'][i]['Channels'][channel]['Size'] = WaveformDuration
                sequence['SequenceElements'][i]['Channels'][channel]['Waveform'] = np.zeros((1,WaveformDuration))
                sequence['SequenceElements'][i]['Channels'][channel]['Marker_1'] = []
                sequence['SequenceElements'][i]['Channels'][channel]['Marker_2'] = []

    # Set the Amplitude, Offset, Delay, Output of sequence['Channels']
    for channel in range(1:5):
        sequence['Channels'][channel] = {}
        sequence['Channels'][channel]['Offset'] = 0.0
        sequence['Channels'][channel]['Delay'] = 0.0
        sequence['Channels'][channel]['Output'] = False
        amplitude = max(np.abs(AmplitudeMin),np.abs(AmplitudeMax))
        sequence['Channels'][channel]['Amplitude'] = max(amplitude,0.02)

    return sequence

if __name__ == '__main__':
    #sion = SionAWG('192.168.1.117', 4000)
    OneGateSpinMap()
