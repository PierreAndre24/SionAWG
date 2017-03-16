# -*- coding: utf-8 -*-
"""
Created on Thu Mar 27 14:51:21 2014

@author: hanno.flentje
"""
import re
import math
import numpy as np
import struct
import itertools
#import pylab

from SocketCom import SocketCom

def test():
    awg=AWGCom('192.168.137.2',4000)
    awg.openCom()
    print awg.readWaveformNames()

    t=np.arange(0,2*math.pi,0.01)
    s= np.sin(t)
    #    print s
    print len(s)
    awg.setRunMode("SEQuence")
    awg.createSequence(SequenceLength=1)

    #    awg.sendMessage("*RST")
    awg.deleteWaveforms('test1')
    awg.newWaveform('test1',len(s))
    awg.transmitWaveformData('test1',s,marker1=np.ones(len(s)))
    awg.setChannelWaveformSequence(Channel=1,WaveformName='test1',SequenceIndex=1)

    second =np.arange(0,1,0.002)
    awg.deleteWaveforms(['test2'])
    awg.newWaveform('test2',len(second))
    awg.transmitWaveformData('test2',second)
    awg.setChannelWaveformSequence(2,'test2',1)
    awg.newWaveform('C1_DATA_1',200000)
    #    awg.sendMessage('*OPC?')
    #    print awg.readMessage()

    #    pylab.plot(t,s)
    #    pylab.show()
    #    awg.deleteWaveforms(names)
    awg.closeCom


class AWGCom(SocketCom):
    """
    The AWGCom object is a tcpip Socket which faciliates communication to a Tektronix AWG.

    After creation of the Instance a Connection has to be opened with the function openCom() to establish a TCPIp connection which afterwards should be closed with the function closeCom.

    To concatenate different commands use the optional parameter stringOnly and pass the commands as a list of the created strings to sendMessage(). If this parameter is not defined or 0, the command will be passed to the AWG when the function is called
    """


    def __init__(self, Ip, Port):
        super(AWGCom,self).__init__(Ip,Port,Delimiter=';:', EndOfMessage='\n')

    def newWaveform(self, name, size, stringOnly=0):
        """
        Creates a new Waveform slot without data in it
        """
        msg='WLIST:WAVeform:NEW "' +name+ '", ' + str(size)+ ', REAL'
        if stringOnly==0:
            self.sendMessage(msg)
        else:
            return msg

    def transmitWaveformData(self, name, data, stringOnly=0, marker1=[], marker2=[]):
        """
        Writes the Data given into the Waveformslot 'name' created by the function newWaveform
        """
        MARKER1= 0b01000000
        MARKER2= 0b10000000
        if (marker1==[]):
            marker1=np.zeros(len(data),dtype=int)
        else:
            marker1=marker1*MARKER1

        if (marker2==[]):
            marker2=np.zeros(len(data),dtype=int)
        else:
            marker2=marker2*MARKER2
        # self.newWaveform(name,len(data))
        block_data=''
        msgStart=('WLISt:WAVeform:DATA "'+name+'",0,'+str(len(data))+',#'+str(len(str(5*len(data))))+str(5*len(data)))
        for val,m1,m2 in itertools.izip(data,marker1,marker2):
            converted_data=struct.pack('<fB',float(val),m1+m2) # or should work aswell

            block_data = block_data + converted_data
        msg=msgStart+block_data

        if stringOnly==0:
            self.sendMessage(msg)
        else:
            return msg

    def readWaveformNames(self):
        """
        Returns a List of all the Waveformnames (strings without enclosing "s)
        """
        self.sendMessage('WLIST:SIZE?')
        ansr=self.readMessage()
        msg=[]
        for i in xrange (1,int(ansr)+1):
            msg.append('WLIST:NAME? '+str(i))
        self.sendMessage(msg)
        wnames = self.readMessage()
        names=re.findall('".*?"',wnames)
        strippednames=[]
        for name in names:
            strippednames.append(name.rstrip('"').lstrip('"'))
        return strippednames

    def deleteWaveforms(self, Names):
        """
        Deletes a list of Waveforms given to the function as strings
        The names are without the enclosing "s and is compliant with the format returned by the function readWaveformNames.

        Passing a single string will try to delete only this Waveform.
        """
        if isinstance(Names, basestring):
            dlmsg='WLISt:WAVeform:DELete "'+Names+'"'
        else:
            try:
                dlmsg=[]
                for name in Names:
                    dlmsg.append('WLISt:WAVeform:DELete "'+name+'"')
            except TypeError:
                print 'TypeError occourred on Waveform Names in function deleteWaveforms, please ensure that message is a string or a list of strings'
        self.sendMessage(dlmsg)

    def changeChannelDelay(self, Channel, Delay, stringOnly=0):
        """
        Changes the delay of the Channel to 'Delay' picoseconds
        """
        msg='SOURCE'+str(Channel)+':DELAY:ADJUST '+str(Delay)
        if stringOnly==0:
            self.sendMessage(msg)
        else:
            return msg

    def changeChannelPhase(self, Channel, Phase, stringOnly=0):
        """
        Changes the phase of the Channel to Phase in Degrees
        """
        msg='SOURCE'+str(Channel)+':PHASE:ADJUST '+str(Phase)
        if stringOnly==0:
            self.sendMessage(msg)
        else:
            return msg

    def changeChannelAmplitude(self, Channel, Amplitude, stringOnly=0):
        msg='SOURCE'+str(Channel)+':VOLTAGE:AMPLITUDE '+str(Amplitude)

        if stringOnly==0:
            self.sendMessage(msg)
        else:
            return msg

    def changeChannelOffset(self, Channel, Offset, stringOnly=0):
        msg='SOURCE'+str(Channel)+':VOLTAGE:OFFSET '+str(Offset)

        if stringOnly==0:
            self.sendMessage(msg)
        else:
            return msg

    def setChannelWaveformSequence(self, Channel, WaveformName, SequenceIndex=1):
        """
        Puts Waveform 'WaveformName' into Channel 'Channel'.

        If the RunMode is SEQuence, it will use the optional Argument 'SequenceIndex' to determine the element in the sequence.
        """
        #SEQuence:ELEMent1:WAVeform1 "waveseq1_channel1";


        self.sendMessage('SEQuence:ELEMent'+str(SequenceIndex)+':WAVeform'+str(Channel)+' "'+WaveformName+'"')

    def setChannelWaveform(self, Channel, WaveformName):
        """
        Puts Waveform 'WaveformName' into Channel 'Channel'.

        If the RunMode is SEQuence, it will use the optional Argument 'SequenceIndex' to determine the element in the sequence.
        """
        self.sendMessage('SOUR'+str(Channel)+':WAVeform "'+ WaveformName+'"')

    def queryRunMode(self):
        self.sendMessage("AWGControl:RMODe?")
        return self.readMessage()

    def setRunMode(self, RunMode, stringOnly=0):
        """
        Sets the runmode of the machine
        RunModes are : CONTinuous, TRIGgered, GATed, SEQuence, ENHanced
        use CONT for normal operation and SEQuence for sequence operation
        """
        msg = "AWGControl:RMODe "+RunMode

        if stringOnly==0:
            self.sendMessage(msg)
        else:
            return msg

    def setChannelOutput(self, Channel, Output, stringOnly=0):
        """
        Sets the output of the channel
        """
        if Output:
            msg = "OUTPut"+str(Channel)+":STATe ON"
        else:
            msg = "OUTPut"+str(Channel)+":STATe OFF"

        if stringOnly==0:
            self.sendMessage(msg)
        else:
            return msg

    def setOutput(self, Output, stringOnly=0):
        """
        Sets all the outputs
        """
        self.setChannelOutput(1, Output, stringOnly)
        self.setChannelOutput(2, Output, stringOnly)
        self.setChannelOutput(3, Output, stringOnly)
        self.setChannelOutput(4, Output, stringOnly)

    def setOutputFilterChannel(self, Channel, filt, stringOnly=0):
        """
        Sets the filter of the channel output
        """
        msg = ''
        if filt == 'Through' or filt == 'INF':
            msg = "OUTPut"+str(Channel)+":FILTer:LPASs:FREQuency INF"

        if stringOnly==0:
            self.sendMessage(msg)
        else:
            return msg

    def setSourceMarkerDelay(self, Channel, Marker, Delay, stringOnly=0):
        """
        Sets the Delay of the Marker
        """
        msg = "SOURce"+str(Channel)+":MARKer"+str(Marker)+":DELay "+str(Delay)

        if stringOnly==0:
            self.sendMessage(msg)
        else:
            return msg

    def setDirectOutput(self,Channel, State, stringOnly=0):
        """
        This command enables the raw DAC waveform outputs for the specified channel.
        """
        if State:
            msg = "AWGControl:DOUTput"+str(Channel)+":STATe ON"
        else:
            msg = "AWGControl:DOUTput"+str(Channel)+":STATe OFF"

        if stringOnly==0:
            self.sendMessage(msg)
        else:
            return msg

    def setAddInput(self,Channel, State, stringOnly=0):
        """
        This command adds the signal from an external input to the output of the channel.
        """
        if State:
            msg = "SOURce"+str(Channel)+':COMBine:FEED "ESIGnal"'
        else:
            msg = "SOURce"+str(Channel)+':COMBine:FEED ""'

        if stringOnly==0:
            self.sendMessage(msg)
        else:
            return msg

    def setSourceMarkerVoltageHigh(self, Channel, Marker, VoltageHigh, stringOnly=0):
        """
        Sets the VoltageHigh of the Marker
        """
        msg = "SOURce"+str(Channel)+":MARKer"+str(Marker)+":VOLTage:HIGH "+str(VoltageHigh)

        if stringOnly==0:
            self.sendMessage(msg)
        else:
            return msg

    def setSourceMarkerVoltageLow(self, Channel, Marker, VoltageLow, stringOnly=0):
        """
        Sets the VoltageLow of the Marker
        """
        msg = "SOURce"+str(Channel)+":MARKer"+str(Marker)+":VOLTage:LOW "+str(VoltageLow)

        if stringOnly==0:
            self.sendMessage(msg)
        else:
            return msg

    def setSamplingRate(self, Rate, stringOnly=0):
        """
        This command and query sets or returns the sampling frequency of the arbitrary
        waveform generator. Sampling frequency can be set when the internal clock
        source is selected and one of the following conditions is met:
        """
        msg = "SOURce1:FREQuency "+str(Rate)

        if stringOnly==0:
            self.sendMessage(msg)
        else:
            return msg

    def setClockSource(self, Source, stringOnly=0):
        """
        This command and query sets or returns the clock source. When the clock source
        is internal, the arbitrary waveform generator's internal clock is used to generate
        the clock signal. If the clock source is external, the clock signal from an external
        oscillator is used.
        """
        if Source == 'Internal':
            msg = "AWGControl:CLOCk:SOURCe INTernal"
        else:
            msg = "AWGControl:CLOCk:SOURCe EXTernal"

        if stringOnly==0:
            self.sendMessage(msg)
        else:
            return msg

    def setTriggerSource(self, Source, stringOnly=0):
        """
        This command and query sets or returns the trigger source
        """
        if Source == 'Internal':
            msg = "TRIGger:SEQuence:SOURCe INTernal"
        else:
            msg = "TRIGger:SEQuence:SOURCe EXernal"

        if stringOnly==0:
            self.sendMessage(msg)
        else:
            return msg

    def setTriggerLevel(self, Level, stringOnly=0):
        """
        This command and query sets or returns the trigger input level (threshold).
        """

        msg = "TRIGger:SEQuence:LEVel " + str(Level)

        if stringOnly==0:
            self.sendMessage(msg)
        else:
            return msg

    def setTriggerSlope(self, Slope, stringOnly=0):
        """
        This command and query sets or returns the trigger slope. It is used to set polarity in modes other than gated mode.
        """

        if Slope == 'Positive':
            msg = "TRIGger:SEQuence:SLOPe POSitive"
        else:
            msg = "TRIGger:SEQuence:SLOPe NEGative"

        if stringOnly==0:
            self.sendMessage(msg)
        else:
            return msg

    def setTriggerImpedance(self, Impedance, stringOnly=0):
        """
        This command and query sets or returns the trigger impedance. It applies only
        to the external trigger.
        """

        if Impedance == '1k':
            msg = "TRIGger:SEQuence:IMPedance 1000"
        else:
            msg = "TRIGger:SEQuence:IMPedance 50"

        if stringOnly==0:
            self.sendMessage(msg)
        else:
            return msg

    def setEventLevel(self, Level, stringOnly=0):
        """
        This command and query sets or returns the event level.
        """

        msg = "EVENt:LEVel " + str(Level)

        if stringOnly==0:
            self.sendMessage(msg)
        else:
            return msg

    def setEventImpedance(self, Impedance, stringOnly=0):
        """
        This command and query sets or returns the impedance of the external event input. Valid values are 50 ohm or 1 kohm.
        """

        if Impedance == '1k':
            msg = "EVENt:IMPedance 1000"
        else:
            msg = "EVENt:IMPedance 50"

        if stringOnly==0:
            self.sendMessage(msg)
        else:
            return msg

    def setEventJumpTiming(self, JTiming, stringOnly=0):
        """
        This command and query sets or returns the jump timing. Refer to the User Online Help for more information on jump timing.
        """

        if Impedance == 'Async':
            msg = "EVENt:JTIMing ASYNchronous"
        else:
            msg = "EVENt:JTIMing SYNChronous"

        if stringOnly==0:
            self.sendMessage(msg)
        else:
            return msg

    def setEventPolarity(self, JTiming, stringOnly=0):
        """
        This command and query sets or returns the polarity of event signal. The Event Jump is the function to change the sequencing of the waveform by an event signal.
        """

        if Impedance == 'Positive':
            msg = "EVENt:POLarity POSitive"
        else:
            msg = "EVENt:POLarity NEGative"

        if stringOnly==0:
            self.sendMessage(msg)
        else:
            return msg

    def setDCOutputLevel(self, Channel, Level, stringOnly=0):
        """
        This command and query sets or returns the DC output level.
        The value of n = 1|2|3|4.
        <offset>::=<NR3> the value will be between –3.0 V to +5.0 V.
        At *RST, this returns 0 V.
        """

        msg = "AWGControl:DC" + str(Channel) + ":VOLTage:OFFSet " + str(Level)

        if stringOnly==0:
            self.sendMessage(msg)
        else:
            return msg

    def createSequence(self, SequenceLength, stringOnly=0):
        """
        This has to be called to initialize a sequence
        """
        msg = 'SEQuence:LENGth '+ str(SequenceLength)

        if stringOnly==0:
            self.sendMessage(msg)
        else:
            return msg

    def setSeqElementGoto(self, SequenceIndex=1, State=1, Index=1, stringOnly=0):
        """
        Used to set JumpMode for a sequence Element
        States are : 0(OFF) , 1(ON)
        """
        msg1 = "SEQuence:ELEMent"+str(SequenceIndex)+":GOTO:STATe "+str(State)
        msg2 = "SEQuence:ELEMent"+str(SequenceIndex)+":GOTO:INDex "+str(Index)

        if stringOnly==0:
            self.sendMessage(msg1)
            if (State==1):
                self.sendMessage(msg2)
        else:
            return msg1, msg2

    def setSeqElementJump(self, SequenceIndex=1, Type='INDex', Index=1):#TODO implement stringonly
        """
        Used to set JumpMode for a sequence Element
        Types are : INDex , NEXT, OFF
        """
        self.sendMessage("SEQuence:ELEMent"+str(SequenceIndex)+":JTARget:TYPE "+str(Type))
        if (Type=='INDex'):
            self.sendMessage("SEQuence:ELEMent"+str(SequenceIndex)+":JTARget:INDex "+str(Index))

    def setSeqElementLooping(self,SequenceIndex=1,Repeat=1,InfiniteLoop=0):#TODO implement stringonly
        """
        Used to set JumpMode for a sequence Element
        States are : 0(OFF) , 1(ON)
        """

        if (InfiniteLoop==1):
            self.sendMessage("SEQuence:ELEMent"+str(SequenceIndex)+":LOOP:INFinite 1")
        else:
            self.sendMessage("SEQuence:ELEMent"+str(SequenceIndex)+":LOOP:INFinite 0")
            self.sendMessage("SEQuence:ELEMent"+str(SequenceIndex)+":LOOP:COUNt "+str(Repeat))

if __name__=='__main__':
    test()


#        print msg
#        f = open('myfile123.txt','w')
#        f.write(msg)
#        f.close()
