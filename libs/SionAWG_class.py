import numpy as np
from SocketCom import SocketCom
from AWGCom import AWGCom

class SionAWG(AWGCom):
    def __init__(self, Ip, Port):
        super(SionAWG,self).__init__(Ip,Port)
        self.RUN_MODE = Run_Mode()
        self.TRIGGER = Trigger()
        self.EVENT = Event()
        self.TIMING = Timing()
        self.DC_OUTPUT = DC_Output()
        self.C1 = Channel(index = 1)
        self.C2 = Channel(index = 2)
        self.C3 = Channel(index = 3)
        self.C4 = Channel(index = 4)

    def Send_Properties(self):
        """
        Sends to the AWG ALL defined parameters
        """
        self.RUN_MODE.Send_Properties()
        self.TRIGGER.Send_Properties()
        self.EVENT.Send_Properties()
        self.TIMING.Send_Properties()
        self.DC_OUTPUT.Send_Properties()
        self.C1.Send_Properties()
        self.C2.Send_Properties()
        self.C3.Send_Properties()
        self.C4.Send_Properties()

    def Send_Properties_Light(self):
        """
        Sends to the AWG only:
            CHANNEL.OFFSET
            CHANNEL.AMPLITUDE
            CHANNEL.DELAY
            CHANNEL.OUTPUT
        """
        self.RUN_MODE.Send_Properties_Light()
        self.TRIGGER.Send_Properties_Light()
        self.EVENT.Send_Properties_Light()
        self.TIMING.Send_Properties_Light()
        self.DC_OUTPUT.Send_Properties_Light()
        self.C1.Send_Properties_Light()
        self.C2.Send_Properties_Light()
        self.C3.Send_Properties_Light()
        self.C4.Send_Properties_Light()

    def test(self):
        self.openCom()
        print self.readWaveformNames()


        self.setRunMode("SEQuence")
        self.createSequence(SequenceLength=1)

        #    awg.sendMessage("*RST")
        t=np.arange(0,2*np.pi,0.01)
        first = np.sin(t)
        self.deleteWaveforms('test1')
        self.newWaveform('test1', len(first))
        self.transmitWaveformData('test1', first, marker1=np.ones(len(first)))
        self.setChannelWaveformSequence(Channel=1, WaveformName='test1', SequenceIndex=1)

        second = np.arange(0,1,0.002)
        self.deleteWaveforms(['test2'])
        self.newWaveform('test2',len(second))
        self.transmitWaveformData('test2',second)
        self.setChannelWaveformSequence(Channel=2,WaveformName='test2',SequenceIndex=1)

        t=np.arange(0,10*np.pi,0.01)
        third = np.sin(t)
        self.deleteWaveforms('test3')
        self.newWaveform('test3', len(third))
        self.transmitWaveformData('test3', third, marker1=np.ones(len(third)))
        self.setChannelWaveformSequence(Channel=3, WaveformName='test3', SequenceIndex=1)

        fourth = np.arange(0,-0.5,-0.002)
        self.deleteWaveforms(['test4'])
        self.newWaveform('test4',len(fourth))
        self.transmitWaveformData('test4',fourth)
        self.setChannelWaveformSequence(Channel=4,WaveformName='test4',SequenceIndex=1)


        #    awg.sendMessage('*OPC?')
        #    print awg.readMessage()
        #    awg.deleteWaveforms(names)
        self.closeCom()

class Channel:
    def __init__(self, index):
        self.CHANNEL_INDEX = index
        self.OUTPUT = False
        self.AMPLITUDE = 1.0 # Volt
        self.OFFSET = 0.0 # Volt
        self.DELAY = 0.0 # Delay in picoseconds
        self.FILTER = 'Through'
        self.MARKER_1_HIGH = 1.0 # Volt
        self.MARKER_1_LOW = 0.0 # Volt
        self.MARKER_1_DELAY = 0.0 # ns
        self.MARKER_2_HIGH = 1.0 # Volt
        self.MARKER_2_LOW = 0.0 # Volt
        self.MARKER_2_DELAY = 0.0 # ns
        self.ADD_INPUT = False
        self.DIRECT_OUTPUT = False
        #self.PHASE = 0.0 # Phase in degrees

    def Send_Properties(self):
        # light sending
        self.setDirectOutput(self.CHANNEL_INDEX, self.DIRECT_OUTPUT)
        self.changeChannelAmplitude(self.CHANNEL_INDEX, self.AMPLITUDE)
        self.changeChannelOffset(self.CHANNEL_INDEX, self.OFFSET)
        self.changeChannelDelay(self.CHANNEL_INDEX, self.DELAY)
        # other stuff
        self.setOutputChannel(self.CHANNEL_INDEX, self.OUTPUT)
        self.setOutputFilterChannel(self.CHANNEL_INDEX, self.FILTER)
        self.setSourceMarkerVoltageHigh(self.CHANNEL_INDEX, 1, self.MARKER_1_HIGH)
        self.setSourceMarkerVoltageLow(self.CHANNEL_INDEX, 1, self.MARKER_1_LOW)
        self.setSourceMarkerDelay(self.CHANNEL_INDEX, 1, self.MARKER_1_DELAY)
        self.setSourceMarkerVoltageHigh(self.CHANNEL_INDEX, 2, self.MARKER_2_HIGH)
        self.setSourceMarkerVoltageLow(self.CHANNEL_INDEX, 2, self.MARKER_2_LOW)
        self.setSourceMarkerDelay(self.CHANNEL_INDEX, 2, self.MARKER_2_DELAY)
        self.setAddInput(self.CHANNEL_INDEX, self.ADD_INPUT)


    def Send_Properties_Light(self):
        # light sending
        self.setDirectOutput(self.CHANNEL_INDEX, self.DIRECT_OUTPUT)
        self.changeChannelAmplitude(self.CHANNEL_INDEX, self.AMPLITUDE)
        self.changeChannelOffset(self.CHANNEL_INDEX, self.OFFSET)
        self.changeChannelDelay(self.CHANNEL_INDEX, self.DELAY)

class Run_Mode:
    def __init__(self):
        '''
        RunModes are : CONTinuous, TRIGgered, GATed, SEQuence, ENHanced
        '''
        self.MODE = 'SEQuence'

    def Send_Properties(self):
        self.setRunMode(self.MODE)

    def Send_Properties_Light(self):
        pass

class Timing:
    def __init__(self):
        self.SAMPLING_RATE = 1200000000
        self.CLOCK_SOURCE = 'Internal'

    def Send_Properties(self):
        self.setClockSource(self.CLOCK_SOURCE)
        self.setSamplingRate(self.SAMPLING_RATE)

    def Send_Properties_Light(self):
        pass

class Trigger:
    def __init__(self):
        self.SOURCE = 'External'
        self.LEVEL = 1.4
        self.SLOPE = 'Positive'
        self.IMPEDANCE = '1k'

    def Send_Properties(self):
        self.setTriggerSource(self.SOURCE)
        self.setTriggerLevel(self.LEVEL)
        self.setTriggerSlope(self.SLOPE)
        self.setTriggerImpedance(self.IMPEDANCE)

    def Send_Properties_Light(self):
        pass

class Event:
    def __init__(self):
        self.LEVEL = 1.4
        self.POLARITY = 'Positive'
        self.JUMP_TIMING = 'Async'
        self.EVENT_IMPEDANCE = '1k'

    def Send_Properties(self):
        self.setEventLevel(self.LEVEL)
        self.setEventPolarity(self.POLARITY)
        self.setEventJumpTiming(self.JUMP_TIMING)
        self.setEventImpedance(self.EVENT_IMPEDANCE)

    def Send_Properties_Light(self):
        pass

class DC_Output:
    def __init__(self):
        self.DC1 = 0.0
        self.DC2 = 0.0
        self.DC3 = 0.0
        self.DC4 = 0.0

    def Send_Properties(self):
        self.setDCOutputLevel(Channel = 1, Level = self.DC1)
        self.setDCOutputLevel(Channel = 2, Level = self.DC2)
        self.setDCOutputLevel(Channel = 3, Level = self.DC3)
        self.setDCOutputLevel(Channel = 4, Level = self.DC4)

    def Send_Properties_Light(self):
        pass

if __name__ == '__main__':
    sion = SionAWG('192.168.1.117', 4000)
    sion.test()
