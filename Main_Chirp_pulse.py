from __future__ import division
import numpy as np
from libs.SionAWG_class import SionAWG
import matplotlib.pyplot as plt

def ChirpPulse(
        SweepChannel = 1,\
        AmplitudeStart = 0.5, \
        AmplitudeStop = 0.5,\
        AmplitudePowerLaw = float(1.),\
        FrequencyStart = 288.6e6/36.,\
        FrequencyStop = 288.6e6/2,\
        PulseDuration = 500e-9, \
        PulseDelay = 00e-9,\
        WaveformDuration = 8000e-9,
        SamplingFrequency = 3000000000):
    # 'Offset', 'Amplitude', 'Delay', 'Output',
    # 'Name', 'Size',
    # 'Waveform', 'Marker_1', 'Marker_2'

    NumberPoints = int(WaveformDuration * SamplingFrequency)
    wf = {}
    # init channels
    for channel in range(1,3):
        wf[channel] = {}
        wf[channel]['Name'] = 'Channel'+str(channel)
        wf[channel]['Size'] = NumberPoints
        wf[channel]['Waveform'] = np.zeros((NumberPoints,1))
        wf[channel]['Marker_1'] = []
        wf[channel]['Marker_2'] = []

    # Marker_1_1
    marker11 = np.zeros((NumberPoints,1))
    marker11[0:100,0] = 1
    # wf[channel]['Marker_1'] = marker11


    #Generate chirp
    PulseNumberPoints = int(PulseDuration * SamplingFrequency)
    t = np.linspace(0,PulseDuration,PulseNumberPoints)
    f = np.linspace(FrequencyStart,FrequencyStop,PulseNumberPoints)
    y = np.sin(2*np.pi*f*t) * Px(t/PulseDuration, AmplitudePowerLaw, AmplitudeStart, AmplitudeStop)
    ychannel = np.zeros((NumberPoints,1))
    delay = int(PulseDelay * SamplingFrequency)
    ychannel[delay:delay+PulseNumberPoints,0] = y
    # wf[SweepChannel]['Waveform'] = ychannel
    wf[2]['Waveform']  = marker11 * 2

    # corr = np.ones((NumberPoints,1))
    # index = int(PulseNumberPoints/(270.-100.)*(165.-100))
    # corr[0:index] = -0.4
    # wf[SweepChannel]['Waveform'] = ychannel * corr
    wf[SweepChannel]['Waveform'] = ychannel


    # Set the Amplitude, Offset, Delay, Output of wf[channel]
    for channel in range(1,3):
        wf[channel]['Offset'] = 0.0
        wf[channel]['Delay'] = 0.0
        wf[channel]['Output'] = False
        if channel == SweepChannel:
            amplitude = 2 * max(np.abs(AmplitudeStop), np.abs(AmplitudeStart))
            wf[channel]['Amplitude'] = max(amplitude,0.02)
        else:
            wf[channel]['Amplitude'] = 0.02

    # return wf
    return wf, ychannel

def Px(x, n, P0, P1):
    return (P1-P0)*x**n + P0

if __name__ == '__main__':
    # sion = SionAWG('192.168.1.117', 4000)
    sion = SionAWG('10.0.0.4', 4000)

    chirppulse, ychannel = ChirpPulse()

    sion.openCom()
    sion.DeleteAllWaveforms()
    sion.SendSingleWFLight(wf = chirppulse)
    sion.closeCom()

    # chirppulse, ychannel = ChirpPulse()
    # plt.plot(ychannel)
    # plt.xlabel('Time')
    # plt.ylabel('Amplitude')
    # plt.grid(True)
    #
    # plt.show()
