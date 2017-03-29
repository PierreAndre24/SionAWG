from __future__ import division
import numpy as np
from libs.SionAWG_class import SionAWG
import matplotlib.pyplot as plt

def RabiCycle(
        ExchangeTime = 81,\
        RampTime = 1000, \
        VoltageTp = 0.35,\
        VoltageUpDown = 0.45,\
        VoltageST = 0.37,\
        WaveformDuration = 2500,\
        WaitBeforeExchangeTime = 2,\
        WaitAfterExchangeTime = 2,\
        WaitAfterSequence = 2):

    arr = np.zeros((int(WaveformDuration),1))
    Toff = int(WaveformDuration) \
            - int(WaitBeforeExchangeTime) \
            - int(WaitAfterExchangeTime) \
            - int(WaitAfterSequence)\
            - 2 * int(RampTime)\
            - int(ExchangeTime)
    #First ramp
    t = Toff
    arr[t:t + int(RampTime),0] = np.linspace(VoltageTp, VoltageUpDown, int(RampTime))
    #Wait before exchange
    t += int(RampTime)
    arr[t:t + int(WaitBeforeExchangeTime),:] = VoltageUpDown * np.ones((int(WaitBeforeExchangeTime),1))
    #Exchange pulse
    t += int(WaitBeforeExchangeTime)
    arr[t:t+int(ExchangeTime),:] = VoltageST * np.ones((int(ExchangeTime),1))
    #Wait after exchange
    t += int(ExchangeTime)
    arr[t:t + int(WaitAfterExchangeTime),:] = VoltageUpDown * np.ones((int(WaitBeforeExchangeTime),1))
    #Second ramp
    t += int(WaitAfterExchangeTime)
    arr[t:t + int(RampTime),0] = np.linspace(VoltageUpDown, VoltageTp, int(RampTime))
    return arr

def OneGateRabiTime(
        SweepChannel = 1,\
        ExchangeTimeStart = 0, \
        ExchangeTimeStop = 80,\
        RampTime = 1000, \
        VoltageTp = 0.35,\
        VoltageUpDown = 0.45,\
        VoltageST = 0.37,\
        WaveformDuration = 2500,\
        WaitBeforeExchangeTime = 2,\
        WaitAfterExchangeTime = 2,\
        WaitAfterSequence = 2):

    """
    Returns NumberPoints pulses (PulseDuration,PulsePosition) on the gate
    SweepChannel with an amplitude varying from AmplitudeStart to
    AmplitudeStop.
    """

    norm = np.abs(VoltageUpDown)
    ExchangeTimeNumberPoints = ExchangeTimeStop - ExchangeTimeStart + 1
    ExchangeTimePoints = np.linspace(ExchangeTimeStart, ExchangeTimeStop, ExchangeTimeNumberPoints)
    RabiSequences = np.zeros((WaveformDuration,ExchangeTimeNumberPoints))
    for i,t in enumerate(ExchangeTimePoints):
        RabiSequences[:,i] = RabiCycle(
                ExchangeTime = t,\
                RampTime = 1000, \
                VoltageTp = 0.35,\
                VoltageUpDown = 0.45,\
                VoltageST = 0.37,\
                WaveformDuration = 2500,\
                WaitBeforeExchangeTime = 2,\
                WaitAfterExchangeTime = 2,\
                WaitAfterSequence = 2)[:,0]
    RabiSequences = RabiSequences / norm

    # Init the sequence
    sequence = {}
    sequence['WaitingSequenceElement'] = {}
    sequence['SequenceElements'] = {}
    sequence['Channels'] = {}
    sequence['NumberOfElements'] = ExchangeTimeNumberPoints

    # Build WaitingSequenceElement
    wait = {}
    wait['Name'] = 'Wait'
    wait['Size'] = WaveformDuration
    wait['Waveform'] = np.zeros((WaveformDuration,1))
    wait['Marker_1'] = []
    wait['Marker_2'] = []
    sequence['WaitingSequenceElement'] = wait

    # Build SequenceElements
    for i in range(ExchangeTimeNumberPoints):
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
                sequence['SequenceElements'][i]['Channels'][channel]['Waveform'] = RabiSequences[:,i-1]
            else:
                sequence['SequenceElements'][i]['Channels'][channel] = wait

    # Set the Amplitude, Offset, Delay, Output of sequence['Channels']
    for channel in range(1,5):
        sequence['Channels'][channel] = {}
        sequence['Channels'][channel]['Offset'] = 0.0
        sequence['Channels'][channel]['Delay'] = 0.0
        sequence['Channels'][channel]['Output'] = False
        if channel == SweepChannel:
            amplitude = 2 * norm
            sequence['Channels'][channel]['Amplitude'] = max(amplitude,0.02)
        else:
            sequence['Channels'][channel]['Amplitude'] = 0.02

    return sequence
    # return RabiSequences

if __name__ == '__main__':
    sion = SionAWG('192.168.1.117', 4000)

    rabi = OneGateRabiTime(\
		SweepChannel = 1,\
        ExchangeTimeStart = 0, \
        ExchangeTimeStop = 80,\
        RampTime = 1000, \
        VoltageTp = 0.35,\
        VoltageUpDown = 0.48,\
        VoltageST = 0.39,\
        WaveformDuration = 2500,\
        WaitBeforeExchangeTime = 2,\
        WaitAfterExchangeTime = 2,\
        WaitAfterSequence = 2)
    sion.openCom()
    sion.DeleteAllWaveforms()
    sion.SendSequenceLight(sequence = rabi)
    sion.closeCom()


    # ychannel = RabiCycle()
    # plt.plot(ychannel)

    # xyz = OneGateRabiTime(
    #         SweepChannel = 1,\
    #         ExchangeTimeStart = 0, \
    #         ExchangeTimeStop = 80,\
    #         RampTime = 1000, \
    #         VoltageTp = 0.35,\
    #         VoltageUpDown = 0.45,\
    #         VoltageST = 0.37,\
    #         WaveformDuration = 2500,\
    #         WaitBeforeExchangeTime = 2,\
    #         WaitAfterExchangeTime = 2,\
    #         WaitAfterSequence = 2)
    # plt.pcolor(xyz)

    # plt.grid(True)
    # plt.show()
