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

    def DeleteAllWaveforms(self, exceptions = []):
        """
        Delete all waveforms present.
        """

        wfnames = self.readWaveformNames()
        if exceptions == []:
            for wfname in wfnames:
                if wfname[0] != '*':
                    self.deleteWaveforms(wfname)
        else:
            for wfname in wfnames:
                if wfname not in exceptions:
                    if wfname[0] != '*':
                        self.deleteWaveforms(wfname)




    def SendSequenceLight(self, sequence):
        """
        sequence is a dictionnary with those entries:
            - 'NumberOfElements'
            - 'SequenceElements' = dictionnary of the SequenceElement
            - 'Channels' = 4 dictionnaries of 'Offset', 'Amplitude', 'Delay', 'Output'
            - 'WaitingSequenceElement' = dict of 'Name', 'Size','Waveform', 'Marker_1', 'Marker_2'
            used to wait for triggers.

        SequenceElement is a dictionnary with:
            - 'Index'
            - 'Channels' = 4 dictionnaries of 'Name', 'Size','Waveform', 'Marker_1', 'Marker_2'
            Has to be the same definition as WaitingSequenceElement
        """
        # Open the communication


        self.setRunMode("SEQuence")
        self.createSequence(SequenceLength = sequence['NumberOfElements']* 2)

        # Send commands for the offset, amplitude, delay, OUTPUT
        for key in sequence['Channels'].keys(): #[1, 2, 3, 4]
            channel = sequence['Channels'][key]
            self.changeChannelOffset(Channel=key, Offset=channel['Offset'])
            self.changeChannelAmplitude(Channel=key, Amplitude=channel['Amplitude'])
            self.changeChannelDelay(Channel=key, Delay=channel['Delay'])
            self.setChannelOutput(Channel=key, Output=channel['Output'])

        # Transmit the waiting sequence element
        self.newWaveform(\
            name=sequence['WaitingSequenceElement']['Name'], \
            size=sequence['WaitingSequenceElement']['Size'])
        self.transmitWaveformData(\
            name=sequence['WaitingSequenceElement']['Name'], \
            data=sequence['WaitingSequenceElement']['Waveform'], \
            marker1=sequence['WaitingSequenceElement']['Marker_1'], \
            marker2=sequence['WaitingSequenceElement']['Marker_2'])

        # Send all the sequence elements
        for seqel in sequence['SequenceElements'].values(): #seqel is abbreviation for SequenceElement
            waitindex = seqel['Index'] * 2 - 1
            seqelindex = waitindex + 1
            # Wait for trigger
            for channel in range(1,5):
                self.setChannelWaveformSequence(\
                    Channel=channel, \
                    WaveformName=sequence['WaitingSequenceElement']['Name'], \
                    SequenceIndex=waitindex)
            self.setSeqElementJump(\
                SequenceIndex=waitindex, \
                Index=seqelindex)
            self.setSeqElementLooping(\
                SequenceIndex=waitindex,\
                Repeat=1,\
                InfiniteLoop=1)

            # Set up all four channels
            for key in seqel['Channels'].keys(): #seqelch stands for sequence element channel
                # the key = channel
                seqelch = seqel['Channels'][key]
                wfname = seqelch['Name']
                if wfname not in self.readWaveformNames():
                    self.newWaveform(\
                        name=wfname, \
                        size=seqelch['Size'])
                    self.transmitWaveformData(\
                        name=wfname, \
                        data=seqelch['Waveform'], \
                        marker1=seqelch['Marker_1'], \
                        marker2=seqelch['Marker_2'])
                self.setChannelWaveformSequence(\
                    Channel=key, \
                    WaveformName=wfname, \
                    SequenceIndex=seqelindex)
            if seqelindex == 2 * sequence['NumberOfElements']:# Back to 1st element
                self.setSeqElementGoto(\
                    SequenceIndex=seqelindex, \
                    State=1, \
                    Index=1)
            else:
                self.setSeqElementGoto(\
                    SequenceIndex=seqelindex, \
                    State=1, \
                    Index=seqelindex + 1)

    def SendMultiDimensionnalSequenceLight(self, mdsequence, resendstartindex = 0, send_Wait = True):
        """
        sequence is a dictionnary with those entries:
            - 'NumberOfElements' = size of SequenceElement
            - 'SequenceLength' = Number of waveforms played by the awg (no waiting)
            - 'SequenceElements' = dictionnary of the SequenceElement
            - 'Sequence' = dictionnary of the Sequence
            - 'Channels' = 4 dictionnaries of 'Offset', 'Amplitude', 'Delay', 'Output'
            - 'WaitingSequenceElement' = dict of 'Name', 'Size','Waveform', 'Marker_1', 'Marker_2'
            used to wait for triggers.

        SequenceElement is a dictionnary with:
            - 'Name' = dictionnary of 'Name', 'Size','Waveform', 'Marker_1', 'Marker_2'
            Has to be the same definition as WaitingSequenceElement

        Sequence is a dictionnary with:
            - 'Index'
            - 'Channels' = dictionnary of Name of the wf (should be present in SequenceElement)
        """
        # Open the communication


        self.setRunMode("SEQuence")
        self.createSequence(SequenceLength = mdsequence['SequenceLength']* 2)

        # Send commands for the offset, amplitude, delay, OUTPUT
        for key in mdsequence['Channels'].keys(): #[1, 2, 3, 4]
            channel = mdsequence['Channels'][key]
            self.changeChannelOffset(Channel=key, Offset=channel['Offset'])
            self.changeChannelAmplitude(Channel=key, Amplitude=channel['Amplitude'])
            self.changeChannelDelay(Channel=key, Delay=channel['Delay'])
            self.setChannelOutput(Channel=key, Output=channel['Output'])

        # Transmit the waiting mdsequence element
        if resendstartindex == 0:
            self.newWaveform(\
                name=mdsequence['WaitingSequenceElement']['Name'], \
                size=mdsequence['WaitingSequenceElement']['Size'])
            self.transmitWaveformData(\
                name=mdsequence['WaitingSequenceElement']['Name'], \
                data=mdsequence['WaitingSequenceElement']['Waveform'], \
                marker1=mdsequence['WaitingSequenceElement']['Marker_1'], \
                marker2=mdsequence['WaitingSequenceElement']['Marker_2'])

        # Transmit all the mdsequence elements
        if resendstartindex == 0:
            for seqel in mdsequence['SequenceElements'].values(): #seqel is abbreviation for SequenceElement
                wfname = seqel['Name']
                self.newWaveform(\
                    name=wfname, \
                    size=seqel['Size'])
                self.transmitWaveformData(\
                    name=wfname, \
                    data=seqel['Waveform'], \
                    marker1=seqel['Marker_1'], \
                    marker2=seqel['Marker_2'])

        # Send all the mdsequence elements
        for seqel in mdsequence['Sequence'].values(): #seqel is abbreviation for SequenceElement
            waitindex = seqel['Index'] * 2 - 1
            seqelindex = waitindex + 1
            if  waitindex >= resendstartindex:
                if send_Wait:
                # Wait for trigger
                    for channel in range(1,5):
                        self.setChannelWaveformSequence(\
                            Channel=channel, \
                            WaveformName=mdsequence['WaitingSequenceElement']['Name'], \
                            SequenceIndex=waitindex)
                    self.setSeqElementJump(\
                        SequenceIndex=waitindex, \
                        Index=seqelindex)
                    self.setSeqElementLooping(\
                        SequenceIndex=waitindex,\
                        Repeat=1,\
                        InfiniteLoop=1)

                # Set up all four channels
                for key in seqel['Channels'].keys(): #seqelch stands for mdsequence element channel
                    # the key = channel
                    wfname = seqel['Channels'][key]
                    self.setChannelWaveformSequence(\
                        Channel=key, \
                        WaveformName=wfname, \
                        SequenceIndex=seqelindex)
                if seqelindex == 2 * mdsequence['SequenceLength']:# Back to 1st element
                    self.setSeqElementGoto(\
                        SequenceIndex=seqelindex, \
                        State=1, \
                        Index=1)
                else:
                    self.setSeqElementGoto(\
                        SequenceIndex=seqelindex, \
                        State=1, \
                        Index=seqelindex + 1)

    def SendMultiDimensionnalSequenceLight_Pre(self, mdsequence, resendstartindex = 0):
        """
        sequence is a dictionnary with those entries:
            - 'NumberOfElements' = size of SequenceElement
            - 'SequenceLength' = Number of waveforms played by the awg (no waiting)
            - 'SequenceElements' = dictionnary of the SequenceElement
            - 'Sequence' = dictionnary of the Sequence
            - 'Channels' = 4 dictionnaries of 'Offset', 'Amplitude', 'Delay', 'Output'
            - 'WaitingSequenceElement' = dict of 'Name', 'Size','Waveform', 'Marker_1', 'Marker_2'
            used to wait for triggers.

        PreSequenceElement is a dictionnary with channel indexes (1, 2, 3, 4) as keys:
            - i: = dictionnary of 'Name', 'Size','Waveform', 'Marker_1', 'Marker_2'

        SequenceElement is a dictionnary with:
            - 'Name' = dictionnary of 'Name', 'Size','Waveform', 'Marker_1', 'Marker_2'
            Has to be the same definition as WaitingSequenceElement

        Sequence is a dictionnary with:
            - 'Index'
            - 'Channels' = dictionnary of Name of the wf (should be present in SequenceElement)
        """
        # Open the communication


        self.setRunMode("SEQuence")
        self.createSequence(SequenceLength = mdsequence['SequenceLength']* 3)

        # Send commands for the offset, amplitude, delay, OUTPUT
        for key in mdsequence['Channels'].keys(): #[1, 2, 3, 4]
            channel = mdsequence['Channels'][key]
            self.changeChannelOffset(Channel=key, Offset=channel['Offset'])
            self.changeChannelAmplitude(Channel=key, Amplitude=channel['Amplitude'])
            self.changeChannelDelay(Channel=key, Delay=channel['Delay'])
            self.setChannelOutput(Channel=key, Output=channel['Output'])

        # Transmit the waiting mdsequence element
        if resendstartindex == 0:
            # Wait element
            self.newWaveform(\
                name=mdsequence['WaitingSequenceElement']['Name'], \
                size=mdsequence['WaitingSequenceElement']['Size'])
            self.transmitWaveformData(\
                name=mdsequence['WaitingSequenceElement']['Name'], \
                data=mdsequence['WaitingSequenceElement']['Waveform'], \
                marker1=mdsequence['WaitingSequenceElement']['Marker_1'], \
                marker2=mdsequence['WaitingSequenceElement']['Marker_2'])
            # PreSequence element
            for channel in mdsequence['PreSequenceElement'].keys():
                self.newWaveform(\
                    name=mdsequence['PreSequenceElement'][channel]['Name'], \
                    size=mdsequence['PreSequenceElement'][channel]['Size'])
                self.transmitWaveformData(\
                    name=mdsequence['PreSequenceElement'][channel]['Name'], \
                    data=mdsequence['PreSequenceElement'][channel]['Waveform'], \
                    marker1=mdsequence['PreSequenceElement'][channel]['Marker_1'], \
                    marker2=mdsequence['PreSequenceElement'][channel]['Marker_2'])

        # Transmit all the mdsequence elements
        if resendstartindex == 0:
            for seqel in mdsequence['SequenceElements'].values(): #seqel is abbreviation for SequenceElement
                wfname = seqel['Name']
                self.newWaveform(\
                    name=wfname, \
                    size=seqel['Size'])
                self.transmitWaveformData(\
                    name=wfname, \
                    data=seqel['Waveform'], \
                    marker1=seqel['Marker_1'], \
                    marker2=seqel['Marker_2'])

        # Send all the mdsequence elements
        for seqel in mdsequence['Sequence'].values(): #seqel is abbreviation for SequenceElement
            waitindex = seqel['Index'] * 3 - 2
            preindex = waitindex + 1
            seqelindex = preindex + 1
            if  waitindex >= resendstartindex:
                # Wait for trigger
                for channel in range(1,5):
                    self.setChannelWaveformSequence(\
                        Channel=channel, \
                        WaveformName=mdsequence['WaitingSequenceElement']['Name'], \
                        SequenceIndex=waitindex)
                self.setSeqElementJump(\
                    SequenceIndex=waitindex, \
                    Index=preindex)
                self.setSeqElementLooping(\
                    SequenceIndex=waitindex,\
                    Repeat=1,\
                    InfiniteLoop=1)

                # PreSequenceElement
                for channel in range(1,5):
                    self.setChannelWaveformSequence(\
                        Channel=channel, \
                        WaveformName=mdsequence['PreSequenceElement'][channel]['Name'], \
                        SequenceIndex=preindex)
                self.setSeqElementGoto(\
                    SequenceIndex=preindex, \
                    State=1, \
                    Index=seqelindex)

                # Set up all four channels
                for key in seqel['Channels'].keys(): #seqelch stands for mdsequence element channel
                    # the key = channel
                    wfname = seqel['Channels'][key]
                    self.setChannelWaveformSequence(\
                        Channel=key, \
                        WaveformName=wfname, \
                        SequenceIndex=seqelindex)
                if seqelindex == 3 * mdsequence['SequenceLength']:# Back to 1st element
                    self.setSeqElementGoto(\
                        SequenceIndex=seqelindex, \
                        State=1, \
                        Index=1)
                else:
                    self.setSeqElementGoto(\
                        SequenceIndex=seqelindex, \
                        State=1, \
                        Index=seqelindex + 1)

    def SendMultiDimensionnalSequenceLight_PrePost(self, mdsequence, resendstartindex = 0):
        """
        sequence is a dictionnary with those entries:
            - 'NumberOfElements' = size of SequenceElement
            - 'SequenceLength' = Number of waveforms played by the awg (no waiting)
            - 'SequenceElements' = dictionnary of the SequenceElement
            - 'Sequence' = dictionnary of the Sequence
            - 'Channels' = 4 dictionnaries of 'Offset', 'Amplitude', 'Delay', 'Output'
            - 'WaitingSequenceElement' = dict of 'Name', 'Size','Waveform', 'Marker_1', 'Marker_2'
            used to wait for triggers.

        PreSequenceElement and PostSequenceElement are dictionnaries with channel indexes (1, 2, 3, 4) as keys:
            - i: = dictionnary of 'Name', 'Size','Waveform', 'Marker_1', 'Marker_2'

        SequenceElement is a dictionnary with:
            - 'Name' = dictionnary of 'Name', 'Size','Waveform', 'Marker_1', 'Marker_2'
            Has to be the same definition as WaitingSequenceElement

        Sequence is a dictionnary with:
            - 'Index'
            - 'Channels' = dictionnary of Name of the wf (should be present in SequenceElement)
        """
        # Open the communication


        self.setRunMode("SEQuence")
        self.createSequence(SequenceLength = mdsequence['SequenceLength'] * 4)

        # Send commands for the offset, amplitude, delay, OUTPUT
        for key in mdsequence['Channels'].keys(): #[1, 2, 3, 4]
            channel = mdsequence['Channels'][key]
            self.changeChannelOffset(Channel=key, Offset=channel['Offset'])
            self.changeChannelAmplitude(Channel=key, Amplitude=channel['Amplitude'])
            self.changeChannelDelay(Channel=key, Delay=channel['Delay'])
            self.setChannelOutput(Channel=key, Output=channel['Output'])

        # Transmit the WaitingSequenceElement, PreSequenceElement, PostSequenceElement mdsequence elements
        if resendstartindex == 0:
            # Wait element
            self.newWaveform(\
                name=mdsequence['WaitingSequenceElement']['Name'], \
                size=mdsequence['WaitingSequenceElement']['Size'])
            self.transmitWaveformData(\
                name=mdsequence['WaitingSequenceElement']['Name'], \
                data=mdsequence['WaitingSequenceElement']['Waveform'], \
                marker1=mdsequence['WaitingSequenceElement']['Marker_1'], \
                marker2=mdsequence['WaitingSequenceElement']['Marker_2'])
            # PreSequence element
            for channel in mdsequence['PreSequenceElement'].keys():
                self.newWaveform(\
                    name=mdsequence['PreSequenceElement'][channel]['Name'], \
                    size=mdsequence['PreSequenceElement'][channel]['Size'])
                self.transmitWaveformData(\
                    name=mdsequence['PreSequenceElement'][channel]['Name'], \
                    data=mdsequence['PreSequenceElement'][channel]['Waveform'], \
                    marker1=mdsequence['PreSequenceElement'][channel]['Marker_1'], \
                    marker2=mdsequence['PreSequenceElement'][channel]['Marker_2'])
            # PostSequence element
            for channel in mdsequence['PostSequenceElement'].keys():
                self.newWaveform(\
                    name=mdsequence['PostSequenceElement'][channel]['Name'], \
                    size=mdsequence['PostSequenceElement'][channel]['Size'])
                self.transmitWaveformData(\
                    name=mdsequence['PostSequenceElement'][channel]['Name'], \
                    data=mdsequence['PostSequenceElement'][channel]['Waveform'], \
                    marker1=mdsequence['PostSequenceElement'][channel]['Marker_1'], \
                    marker2=mdsequence['PostSequenceElement'][channel]['Marker_2'])

        # Transmit all the mdsequence elements
        if resendstartindex == 0:
            for seqel in mdsequence['SequenceElements'].values(): #seqel is abbreviation for SequenceElement
                wfname = seqel['Name']
                self.newWaveform(\
                    name=wfname, \
                    size=seqel['Size'])
                self.transmitWaveformData(\
                    name=wfname, \
                    data=seqel['Waveform'], \
                    marker1=seqel['Marker_1'], \
                    marker2=seqel['Marker_2'])

        # Send all the mdsequence elements
        for seqel in mdsequence['Sequence'].values(): #seqel is abbreviation for SequenceElement
            # waitindex = seqel['Index'] * 3 - 2
            # preindex = waitindex + 1
            # seqelindex = preindex + 1
            waitindex = seqel['Index'] * 4 - 3
            preindex = waitindex + 1
            seqelindex = preindex + 1
            postindex = seqelindex + 1
            if  waitindex >= resendstartindex:
                # Wait for trigger
                for channel in range(1,5):
                    self.setChannelWaveformSequence(\
                        Channel=channel, \
                        WaveformName=mdsequence['WaitingSequenceElement']['Name'], \
                        SequenceIndex=waitindex)
                self.setSeqElementJump(\
                    SequenceIndex=waitindex, \
                    Index=preindex)
                self.setSeqElementLooping(\
                    SequenceIndex=waitindex,\
                    Repeat=1,\
                    InfiniteLoop=1)

                # PreSequenceElement
                for channel in range(1,5):
                    self.setChannelWaveformSequence(\
                        Channel=channel, \
                        WaveformName=mdsequence['PreSequenceElement'][channel]['Name'], \
                        SequenceIndex=preindex)
                self.setSeqElementGoto(\
                    SequenceIndex=preindex, \
                    State=1, \
                    Index=seqelindex)

                # Set up all four channels
                for key in seqel['Channels'].keys(): #seqelch stands for mdsequence element channel
                    # the key = channel
                    wfname = seqel['Channels'][key]
                    self.setChannelWaveformSequence(\
                        Channel=key, \
                        WaveformName=wfname, \
                        SequenceIndex=seqelindex)
                self.setSeqElementGoto(\
                    SequenceIndex=seqelindex, \
                    State=1, \
                    Index=postindex)

                # PostSequenceElement
                for channel in range(1,5):
                    self.setChannelWaveformSequence(\
                        Channel=channel, \
                        WaveformName=mdsequence['PostSequenceElement'][channel]['Name'], \
                        SequenceIndex=postindex)
                if postindex == 4 * mdsequence['SequenceLength']:# Back to 1st element
                    self.setSeqElementGoto(\
                        SequenceIndex=postindex, \
                        State=1, \
                        Index=1)
                else:
                    self.setSeqElementGoto(\
                        SequenceIndex=postindex, \
                        State=1, \
                        Index=postindex + 1)

    def SendSingleWFLight(self, wf):
        """
        wf is a dictionnary with those entries:
            - 'Channels' = 4 objects with properties 'Offset', 'Amplitude', 'Delay', 'Output', 'Name', 'Size','Waveform', 'Marker_1', 'Marker_2'
        """
        # Open the communication


        self.setRunMode("CONTinuous")

        # Send commands for the offset, amplitude, delay, OUTPUT
        for key in wf.keys(): #[1, 2, 3, 4]
            channel = wf[key]
            self.changeChannelOffset(Channel=key, Offset=channel['Offset'])
            self.changeChannelAmplitude(Channel=key, Amplitude=channel['Amplitude'])
            self.changeChannelDelay(Channel=key, Delay=channel['Delay'])
            self.setChannelOutput(Channel=key, Output=channel['Output'])

        # Set up all four channels
        for key in wf.keys(): #seqelch stands for sequence element channel
            # the key = channel
            wfch = wf[key]
            wfname = wfch['Name']
            if wfname not in self.readWaveformNames():
                self.newWaveform(\
                    name=wfname, \
                    size=wfch['Size'])
                self.transmitWaveformData(\
                    name=wfname, \
                    data=wfch['Waveform'], \
                    marker1=wfch['Marker_1'], \
                    marker2=wfch['Marker_2'])
            self.setChannelWaveform(\
                Channel=key, \
                WaveformName=wfname)



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
