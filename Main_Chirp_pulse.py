from __future__ import division
import numpy as np
from libs.SionAWG_class import SionAWG
import matplotlib.pyplot as plt

def ChirpPulse(
        SweepChannel = 1,\
        AmplitudeStart = 0.5, \
        AmplitudeStop = 0.1,\
        AmplitudePowerLaw = float(2/3`),\
        FrequencyStart = 0.01e8,\
        FrequencyStop = 1e8,\
        PulseDuration = 500e-9, \
        PulseDelay = 00e-9,\
        WaveformDuration = 500e-9,
        SamplingFrequency = 12000000000):
    # 'Offset', 'Amplitude', 'Delay', 'Output',
    # 'Name', 'Size',
    # 'Waveform', 'Marker_1', 'Marker_2'

    NumberPoints = int(WaveformDuration * SamplingFrequency)
    wf = {}
    # init channels
    for channel in range(1,5):
        wf[channel] = {}
        wf[channel]['Name'] = 'Channel'+str(channel)
        wf[channel]['Size'] = NumberPoints
        wf[channel]['Waveform'] = np.zeros((NumberPoints,1))
        wf[channel]['Marker_1'] = []
        wf[channel]['Marker_2'] = []

    # Marker_1_1
    marker11 = np.zeros((NumberPoints,1))
    marker11[0:100,0] = 1
    wf[channel]['Marker_1'] = marker11

    #Generate chirp
    PulseNumberPoints = int(PulseDuration * SamplingFrequency)
    t = np.linspace(0,PulseDuration,PulseNumberPoints)
    f = np.linspace(FrequencyStart,FrequencyStop,PulseNumberPoints)
    y = np.sin(2*np.pi*f*t) * Px(t/PulseDuration, AmplitudePowerLaw, AmplitudeStart, AmplitudeStop)
    ychannel = np.zeros((NumberPoints,1))
    delay = int(PulseDelay * SamplingFrequency)
    ychannel[delay:delay+PulseNumberPoints,0] = y
    wf[SweepChannel]['Waveform'] = ychannel
    wf[2]['Waveform']  = marker11 * 2

    # Set the Amplitude, Offset, Delay, Output of wf[channel]
    for channel in range(1,5):
        wf[channel]['Offset'] = 0.0
        wf[channel]['Delay'] = 0.0
        wf[channel]['Output'] = False
        if channel == SweepChannel:
            amplitude = 2 * max(np.abs(AmplitudeStop), np.abs(AmplitudeStart))
            wf[channel]['Amplitude'] = max(amplitude,0.02)
        else:
            wf[channel]['Amplitude'] = 0.02

    # return wf
    return ychannel

def Px(x, n, P0, P1):
    return (P1-P0)*x**n + P0

if __name__ == '__main__':
    # sion = SionAWG('192.168.1.117', 4000)
    # sion = SionAWG('10.0.0.4', 4000)
    #
    # chirppulse = ChirpPulse()
    #
    # sion.openCom()
    # sion.DeleteAllWaveforms()
    # sion.SendSingleWFLight(wf = chirppulse)
    # sion.closeCom()

    ychannel = ChirpPulse()
    plt.plot(ychannel)
    plt.xlabel('Time')
    plt.ylabel('Amplitude')
    plt.grid(True)

    plt.show()
