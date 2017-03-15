# -*- coding: utf-8 -*-
"""
Created on Thu Apr 07 11:23:54 2016

@author: manip.batm
"""

import re
import math
import numpy as np
import struct
import itertools
import pylab
import matplotlib.pyplot as plt
from operator import sub
from scipy import *
from SocketCom import SocketCom
from AWGCom import AWGCom
from jump import jump
from sweep_n_step import sweep_n_step
from rabi import rabi
from multi_rabi4 import multi_rabi
from multi_rabi_waitingtime import multi_rabi_waitingtime
from multi_rabi_amplitude import multi_rabi_amplitude
from step2_multiwaitingtime import step2_multiwaitingtime
from trigg_channel import trigg_channel


def wait(time,AWG_SR,ADC_SR,C1_value,C2_value, default_value):
    
    C1_DATA=np.ones((1,int(time*AWG_SR/ADC_SR)))*C1_value
    C2_DATA=np.ones((1,int(time*AWG_SR/ADC_SR)))*C2_value
    C3_DATA=np.ones((1,int(time*AWG_SR/ADC_SR)))*default_value
    C4_DATA=np.ones((1,int(time*AWG_SR/ADC_SR)))*default_value

    
    MARKER_C1_1=np.zeros((1,int(time*AWG_SR/ADC_SR)))
    MARKER_C2_1=np.zeros((1,int(time*AWG_SR/ADC_SR)))
    MARKER_C3_1=np.zeros((1,int(time*AWG_SR/ADC_SR)))
    MARKER_C4_1=np.zeros((1,int(time*AWG_SR/ADC_SR)))

    
    MARKER_C1_2=np.zeros((1,int(time*AWG_SR/ADC_SR)))
    MARKER_C2_2=np.zeros((1,int(time*AWG_SR/ADC_SR)))
    MARKER_C3_2=np.zeros((1,int(time*AWG_SR/ADC_SR)))
    MARKER_C4_2=np.zeros((1,int(time*AWG_SR/ADC_SR)))
    
    SIZE=C1_DATA.size;


    OFFSET = [0,0,0,0];
    
    return C1_DATA,C2_DATA,C3_DATA,C4_DATA,MARKER_C1_1,MARKER_C2_1,MARKER_C3_1,MARKER_C4_1,MARKER_C1_2,MARKER_C2_2,MARKER_C3_2,MARKER_C4_2,OFFSET,SIZE,time
    


def SendWaveForm(N_step):

    awg=AWGCom('192.168.137.2',4000)
    awg.openCom()

    awg.setRunMode("SEQuence")
    names=awg.readWaveformNames()
    

    send_CH4 = 0
    send_CH3 = 0
    send_CH2 = 0
    send_CH1 = 0
 
    
    awg.deleteWaveforms(names)
    awg.createSequence(SequenceLength=2*N_step+3)


    ######### sequence of the ramp###########

    awg.newWaveform('waveseq'+str(1)+'_channel1',SIZE[0][1])
    awg.transmitWaveformData('waveseq'+str(1)+'_channel1',C1_DATA[0],marker1=MARKER_C1_1[0],marker2=MARKER_C1_2[0])
    awg.setChannelWaveformSequence(Channel=1,WaveformName='waveseq'+str(1)+'_channel1',SequenceIndex=1)


    awg.newWaveform('waveseq'+str(1)+'_channel2',SIZE[0][1])
    awg.transmitWaveformData('waveseq'+str(1)+'_channel2',C2_DATA[0],marker1=MARKER_C2_1[0],marker2=MARKER_C2_2[0])
    awg.setChannelWaveformSequence(Channel=2,WaveformName='waveseq'+str(1)+'_channel2',SequenceIndex=1)

    awg.newWaveform('waveseq'+str(1)+'_channel3',SIZE[0][1])
    awg.transmitWaveformData('waveseq'+str(1)+'_channel3',C3_DATA[0],marker1=MARKER_C3_1[0],marker2=MARKER_C3_2[0])
    awg.setChannelWaveformSequence(Channel=3,WaveformName='waveseq'+str(1)+'_channel3',SequenceIndex=1)

    awg.newWaveform('waveseq'+str(1)+'_channel4',SIZE[0][1])
    awg.transmitWaveformData('waveseq'+str(1)+'_channel4',C4_DATA[0],marker1=MARKER_C4_1[0],marker2=MARKER_C4_2[0])
    awg.setChannelWaveformSequence(Channel=4,WaveformName='waveseq'+str(1)+'_channel4', SequenceIndex=1)
   
   
   
    awg.setChannelWaveformSequence(Channel=1,WaveformName='waveseq'+str(1)+'_channel1',SequenceIndex=2)
    awg.setChannelWaveformSequence(Channel=2,WaveformName='waveseq'+str(1)+'_channel2',SequenceIndex=2)
    awg.setChannelWaveformSequence(Channel=3,WaveformName='waveseq'+str(1)+'_channel3',SequenceIndex=2)
    awg.setChannelWaveformSequence(Channel=4,WaveformName='waveseq'+str(1)+'_channel4', SequenceIndex=2)





############ WAIT ##############
    if send_CH1==0:
        awg.newWaveform('WAIT'+str(time)+'CH1',SIZE_WAIT)
        awg.transmitWaveformData('WAIT'+str(time)+'CH1',C1_DATA_WAIT[0],marker1=MARKER_C1_1_WAIT[0],marker2=MARKER_C1_2_WAIT[0])
        awg.setChannelWaveformSequence(Channel=1,WaveformName='WAIT'+str(time)+'CH1',SequenceIndex=4)
    
    if send_CH2==0:
        awg.newWaveform('WAIT'+str(time)+'CH2',SIZE_WAIT)
        awg.transmitWaveformData('WAIT'+str(time)+'CH2',C2_DATA_WAIT[0],marker1=MARKER_C2_1_WAIT[0],marker2=MARKER_C2_2_WAIT[0])
        awg.setChannelWaveformSequence(Channel=2,WaveformName='WAIT'+str(time)+'CH2',SequenceIndex=4)
   
    if send_CH3==0:
        awg.newWaveform('WAIT'+str(time)+'CH3',SIZE_WAIT)
        awg.transmitWaveformData('WAIT'+str(time)+'CH3',C3_DATA_WAIT[0],marker1=MARKER_C3_1_WAIT[0],marker2=MARKER_C3_2_WAIT[0])
        awg.setChannelWaveformSequence(Channel=3,WaveformName='WAIT'+str(time)+'CH3',SequenceIndex=4)

    if send_CH4==0:
        awg.newWaveform('WAIT'+str(time)+'CH4',SIZE_WAIT)
        awg.transmitWaveformData('WAIT'+str(time)+'CH4',C4_DATA_WAIT[0],marker1=MARKER_C4_1_WAIT[0],marker2=MARKER_C4_2_WAIT[0])
        awg.setChannelWaveformSequence(Channel=4,WaveformName='WAIT'+str(time)+'CH4',SequenceIndex=4)
    
#    
#    
#    awg.setChannelWaveformSequence(Channel=1,WaveformName='WAIT'+str(time)+'CH1',SequenceIndex=3)
#    awg.setChannelWaveformSequence(Channel=2,WaveformName='WAIT'+str(time)+'CH2',SequenceIndex=3)
#    awg.setChannelWaveformSequence(Channel=3,WaveformName='WAIT'+str(time)+'CH3',SequenceIndex=3)
#    awg.setChannelWaveformSequence(Channel=4,WaveformName='WAIT'+str(time)+'CH4',SequenceIndex=3)


    
    

    j=1       
    for i in range(3,2*N_step+2,2):
    
    ######### sequence of the ramp###########
        
        awg.newWaveform('waveseq'+str(i)+'_channel1',SIZE[0][1])
        awg.transmitWaveformData('waveseq'+str(i)+'_channel1',C1_DATA[j],marker1=MARKER_C1_1[j],marker2=MARKER_C1_2[j])
        awg.setChannelWaveformSequence(Channel=1,WaveformName='waveseq'+str(i)+'_channel1',SequenceIndex=i)
        
        
        awg.newWaveform('waveseq'+str(i)+'_channel2',SIZE[0][1])
        awg.transmitWaveformData('waveseq'+str(i)+'_channel2',C2_DATA[j],marker1=MARKER_C2_1[j],marker2=MARKER_C2_2[j])
        awg.setChannelWaveformSequence(Channel=2,WaveformName='waveseq'+str(i)+'_channel2',SequenceIndex=i)
        
        awg.newWaveform('waveseq'+str(i)+'_channel3',SIZE[0][1])
        awg.transmitWaveformData('waveseq'+str(i)+'_channel3',C3_DATA[j],marker1=MARKER_C3_1[j],marker2=MARKER_C3_2[j])
        awg.setChannelWaveformSequence(Channel=3,WaveformName='waveseq'+str(i)+'_channel3',SequenceIndex=i)
        
        awg.newWaveform('waveseq'+str(i)+'_channel4',SIZE[0][1])
        awg.transmitWaveformData('waveseq'+str(i)+'_channel4',C4_DATA[j],marker1=MARKER_C4_1[j],marker2=MARKER_C4_2[j])
        awg.setChannelWaveformSequence(Channel=4,WaveformName='waveseq'+str(i)+'_channel4', SequenceIndex=i)
        
        
        
    ############ WAIT ##############
###        
        awg.setChannelWaveformSequence(Channel=1,WaveformName='WAIT'+str(time)+'CH1',SequenceIndex=i+1)       
        awg.setChannelWaveformSequence(Channel=2,WaveformName='WAIT'+str(time)+'CH2',SequenceIndex=i+1)        
        awg.setChannelWaveformSequence(Channel=3,WaveformName='WAIT'+str(time)+'CH3',SequenceIndex=i+1)        
        awg.setChannelWaveformSequence(Channel=4,WaveformName='WAIT'+str(time)+'CH4',SequenceIndex=i+1)    
                
        j=j+1
        
        
 ############ WAIT ##############
###        
    awg.setChannelWaveformSequence(Channel=1,WaveformName='WAIT'+str(time)+'CH1',SequenceIndex=2*N_step+3)    
    awg.setChannelWaveformSequence(Channel=2,WaveformName='WAIT'+str(time)+'CH2',SequenceIndex=2*N_step+3)    
    awg.setChannelWaveformSequence(Channel=3,WaveformName='WAIT'+str(time)+'CH3',SequenceIndex=2*N_step+3)    
    awg.setChannelWaveformSequence(Channel=4,WaveformName='WAIT'+str(time)+'CH4',SequenceIndex=2*N_step+3)    
           

    awg.setSeqElementLooping(SequenceIndex=1,Repeat=0,InfiniteLoop=1)
    awg.setSeqElementJump(SequenceIndex=1,Type='INDex',Index=2)
    awg.setSeqElementGoto(SequenceIndex=1,State=0,Index=0)

    
    awg.setSeqElementLooping(SequenceIndex=2,Repeat=0,InfiniteLoop=1)
    awg.setSeqElementJump(SequenceIndex=2,Type='INDex',Index=3)
    awg.setSeqElementGoto(SequenceIndex=2,State=0,Index=0)
    
#    awg.setSeqElementLooping(SequenceIndex=3,Repeat=2500,InfiniteLoop=0)
#    awg.setSeqElementJump(SequenceIndex=3,Type='INDex',Index=2)
#    awg.setSeqElementGoto(SequenceIndex=3,State=1,Index=4)
    
    
    
    for i in range(3,2*N_step+1,1):
        
        awg.setSeqElementLooping(SequenceIndex=i,Repeat=1,InfiniteLoop=0)
        awg.setSeqElementJump(SequenceIndex=i,Type='INDex',Index=2)
        awg.setSeqElementGoto(SequenceIndex=i,State=1,Index=i+1)
      

    awg.setSeqElementLooping(SequenceIndex=2*N_step+1,Repeat=1,InfiniteLoop=0)
    awg.setSeqElementJump(SequenceIndex=2*N_step+1,Type='INDex',Index=2)
    awg.setSeqElementGoto(SequenceIndex=2*N_step+1,State=1,Index=2*N_step+2)
    
    ############ WAIT ##############
    
    awg.setSeqElementLooping(SequenceIndex=2*N_step+2,Repeat=1,InfiniteLoop=0)
    awg.setSeqElementJump(SequenceIndex=2*N_step+2,Type='INDex',Index=2)
    awg.setSeqElementGoto(SequenceIndex=2*N_step+2,State=1,Index=2*N_step+3)    


    awg.setSeqElementLooping(SequenceIndex=2*N_step+3,Repeat=25,InfiniteLoop=0)
    awg.setSeqElementJump(SequenceIndex=2*N_step+3,Type='INDex',Index=2)
    awg.setSeqElementGoto(SequenceIndex=2*N_step+3,State=1,Index=3)  
#
    
    
    
    awg.changeChannelAmplitude(Channel=1,Amplitude=AMPLITUDE[0][0],stringOnly=0)
    awg.changeChannelAmplitude(Channel=2,Amplitude=AMPLITUDE[0][1],stringOnly=0)
    awg.changeChannelAmplitude(Channel=3,Amplitude=AMPLITUDE[0][2],stringOnly=0)
    awg.changeChannelAmplitude(Channel=4,Amplitude=AMPLITUDE[0][3],stringOnly=0)

    awg.changeChannelOffset(Channel=1,Offset=OFFSET[0],stringOnly=0)
    awg.changeChannelOffset(Channel=2,Offset=OFFSET[1],stringOnly=0)
    awg.changeChannelOffset(Channel=3,Offset=OFFSET[2],stringOnly=0)
    awg.changeChannelOffset(Channel=4,Offset=OFFSET[3],stringOnly=0)


    awg.closeCom


if __name__=='__main__':

#    db_atenuation_blue=db_atenuation_green=db_atenuation_red=141.667;####10db
#    db_atenuation_black=158.58;####10db

#    db_atenuation_blue=db_atenuation_green=db_atenuation_red=89.1266;####6db
#    db_atenuation_black=100;####6db

    db_atenuation_blue=db_atenuation_green=db_atenuation_red=63.15;####3db
    db_atenuation_black=70.833;####3db


##################################
#######    waiting time    #######
###################################



    ###############################
##       S-T mixing
#    ###############################
#########
#    X_A =X_B =X_C =X_D =X_E =X_F =X_H =X_I =X_J =-0.03216*db_atenuation_blue/2;
##    X_E =-0.01437*db_atenuation_blue/2;
##    X_F =-0.01494*db_atenuation_blue/2;
#    X_G =-0.0*db_atenuation_blue/2;
#    
#    
#    Y_A =Y_B =Y_C =Y_D =Y_E =Y_F =Y_H =Y_I =Y_J =-0.01457*db_atenuation_black/2;
##    Y_E =-0.02998*db_atenuation_black/2;
##    Y_F =-0.0273*db_atenuation_black/2;
#    Y_G =-0.044*db_atenuation_black/2;
###    
#
#    N_step = 100
#
#    wait_A_start=25.9e-6
#    wait_AB_start=0e-9
#    wait_B_start=0e-6
#    wait_BC_start=0e-6
#    wait_C_start=0e-9
#    wait_CD_start=0e-9
#    wait_D_start=0e-9
#    wait_DE_start=0e-9
#    wait_E_start=0e-6
#    wait_EF_start=0e-9
#    wait_F_start=0e-9
#    wait_FG_start=0e-9
#    wait_G_start=1e-9#####
#    wait_GH_start=0e-9 
#    wait_H_start=0e-9
#    wait_HI_start=0e-9
#    wait_I_start=0e-9
#    wait_IJ_start=0e-9
#    wait_J_start=99e-9
#           
#    
#    wait_A_stop=25.9e-6
#    wait_AB_stop=0e-9
#    wait_B_stop=0e-6
#    wait_BC_stop=0e-6
#    wait_C_stop=0e-9
#    wait_CD_stop=0e-9
#    wait_D_stop=0e-9
#    wait_DE_stop=0e-9
#    wait_E_stop=0e-6
#    wait_EF_stop=0e-9
#    wait_F_stop=0e-9
#    wait_FG_stop=0e-9
#    wait_G_stop=100e-9#####
#    wait_GH_stop=0e-9 
#    wait_H_stop=0e-9
#    wait_HI_stop=0e-9
#    wait_I_stop=0e-9
#    wait_IJ_stop=0e-9
#    wait_J_stop=1e-9   

#########################################


#    #################################
#####        ramp  adiabatic 
    #################################
#####
#
#    X_A=X_B=X_C=X_D=X_E=X_F =X_J=-0.03216*db_atenuation_blue/2;
#    X_G=X_I=-0.02406*db_atenuation_blue/2;
#    X_H=-0.0*db_atenuation_blue/2;
#    
#    
#    Y_A=Y_B=Y_C=Y_D=Y_E=Y_F =Y_J =-0.01457*db_atenuation_black/2;
#    Y_I=Y_G=-0.022*db_atenuation_black/2;
#    Y_H=-0.044*db_atenuation_black/2;
#   
#   
#    N_step = 101
#
#
#    wait_A_start=24e-6
#    wait_AB_start=0e-9
#    wait_B_start=0e-6
#    wait_BC_start=0e-9
#    wait_C_start=0e-9
#    wait_CD_start=0e-9
#    wait_D_start=0e-9
#    wait_DE_start=0e-9
#    wait_E_start=1e-9
#    wait_EF_start=0e-9
#    wait_F_start=0e-9
#    wait_FG_start=0e-9
#    wait_G_start=1e-9
#    wait_GH_start=10e-9##
#    wait_H_start=100e-9
#    wait_HI_start=10e-9##
#    wait_I_start=1e-9
#    wait_IJ_start=0e-9
#    wait_J_start=1878e-9
#        
#    
#    
#    wait_A_stop=24e-6
#    wait_AB_stop=0e-9
#    wait_B_stop=0e-6
#    wait_BC_stop=0e-9
#    wait_C_stop=0e-9
#    wait_CD_stop=0e-9
#    wait_D_stop=0e-9
#    wait_DE_stop=0e-6
#    wait_E_stop=0e-9
#    wait_EF_stop=0e-9
#    wait_F_stop=0e-9
#    wait_FG_stop=0e-9
#    wait_G_stop=1e-9
#    wait_GH_stop=510e-9##
#    wait_H_stop=100e-9
#    wait_HI_stop=510e-9##
#    wait_I_stop=1e-9
#    wait_IJ_stop=0e-9
#    wait_J_stop=878e-9   

#    #################################
#####       adiabatic S pumping ?
    #################################
####
##
#    X_A=X_B=X_C=X_D=X_E=X_H=-0.01142*db_atenuation_blue/2;
#    X_F=-0.01256*db_atenuation_blue/2;
#    X_G=-0.01428*db_atenuation_blue/2;
#
#    
#    
#    Y_A=Y_B=Y_C=Y_D=Y_E=Y_H=-0.02975*db_atenuation_black/2;
#    Y_F=-0.02875*db_atenuation_black/2;
#    Y_G=-0.02724*db_atenuation_black/2;
#   
#    N_step = 51
#
#    wait_A_start=26e-6
#    wait_AB_start=0e-9
#    wait_B_start=0e-6
#    wait_BC_start=0e-9
#    wait_C_start=0e-9
#    wait_CD_start=0e-9
#    wait_D_start=0e-9
#    wait_DE_start=0e-9
#    wait_E_start=0e-9
#    wait_EF_start=0e-9###
#    wait_F_start=1e-9
#    wait_FG_start=2e-9###
#    wait_G_start=5e-9
#    wait_GH_start=0e-9
#    wait_H_start=10e-9
#        
#    
#    
#    wait_A_stop=26e-6
#    wait_AB_stop=0e-9
#    wait_B_stop=0e-6
#    wait_BC_stop=0e-9
#    wait_C_stop=0e-9
#    wait_CD_stop=0e-9
#    wait_D_stop=0e-9
#    wait_DE_stop=0e-6
#    wait_E_stop=0e-9
#    wait_EF_stop=0e-9###
#    wait_F_stop=1e-9
#    wait_FG_stop=202e-9###
#    wait_G_stop=5e-9
#    wait_GH_stop=0e-9
#    wait_H_stop=10e-9
#
#

    #################################
####       adiabatic T pumping ?
    #################################
#####
###
#    X_A=X_B=X_C=X_F=X_H=-0.01265*db_atenuation_blue/2;
#    X_D = -0.01647*db_atenuation_blue/2;
#    X_E = -0.02011*db_atenuation_blue/2;
#    X_F = -0.01571*db_atenuation_blue/2;
#    X_G = -0.0136*db_atenuation_blue/2;
##
##    
##    
#    Y_A=Y_B=Y_C=Y_F=Y_H=-0.03335*db_atenuation_black/2;
#    Y_D = -0.03711*db_atenuation_black/2;
#    Y_E = -0.03418*db_atenuation_black/2;
#    Y_F = -0.0301*db_atenuation_black/2;
#    Y_G = -0.0324*db_atenuation_black/2;
##   
#    N_step = 51
#
#
#    wait_A_start=10e-9
#    wait_AB_start=0e-9
#    wait_B_start=0e-6
#    wait_BC_start=0e-9
#    wait_C_start=0e-9
#    wait_CD_start=0e-9
#    wait_D_start=25e-6
#    wait_DE_start=0e-9
#    wait_E_start=5e-6
#    wait_EF_start=0e-9
#    wait_F_start=1e-9
#    wait_FG_start=2e-9###
#    wait_G_start=1e-9
#    wait_GH_start=0e-9
#    wait_H_start=10e-9
#        
#    
#    
#    wait_A_stop=10e-9
#    wait_AB_stop=0e-9
#    wait_B_stop=0e-6
#    wait_BC_stop=0e-9
#    wait_C_stop=0e-9
#    wait_CD_stop=0e-9
#    wait_D_stop=25e-6
#    wait_DE_stop=0e-6
#    wait_E_stop=5e-6
#    wait_EF_stop=0e-9
#    wait_F_stop=1e-9
#    wait_FG_stop=202e-9###
#    wait_G_stop=1e-9
#    wait_GH_stop=0e-9
#    wait_H_stop=10e-9

####################################
##
#           Exchange oscilllations
##
###   ###########################

#    X_A=X_G=X_H=-0.009985*db_atenuation_blue/2;
#    X_B=X_F=-0.01494*db_atenuation_blue/2;
#    X_D=-0.00306*db_atenuation_blue/2;
#    X_C=X_E=-0.04425*db_atenuation_blue/2;
#        
#    
#    Y_A=Y_G=Y_H=-0.0333*db_atenuation_black/2;
#    Y_B=Y_F=-0.0287*db_atenuation_black/2;
#    Y_D=-0.03894*db_atenuation_black/2;
#    Y_C=Y_E=-0.001104*db_atenuation_black/2;
#

#
#    N_step = 81
#    
####   
###
##
##
#    wait_A_start=24.98e-6
#    wait_AB_start=0e-9
#    wait_B_start=2e-9
#    wait_BC_start=500e-9
#    wait_C_start=2e-9
#    wait_CD_start=0e-9
#    wait_D_start=2e-9###
#    wait_DE_start=0e-9
#    wait_E_start=2e-9
#    wait_EF_start=500e-9
#    wait_F_start=2e-9
#    wait_FG_start=0e-9
#    wait_G_start=0e-9
#    wait_GH_start=0e-9
#    wait_H_start=0e-9
#    wait_HI_start=0e-9
#    wait_I_start=0e-9
#    wait_IJ_start=0e-9
#    wait_J_start=10e-9
#        
#                  
#    
#    wait_A_stop=24.98e-6
#    wait_AB_stop=0e-9
#    wait_B_stop=2e-9
#    wait_BC_stop=500e-9
#    wait_C_stop=2e-9
#    wait_CD_stop=0e-9
#    wait_D_stop=2e-9###
#    wait_DE_stop=0e-9
#    wait_E_stop=2e-9
#    wait_EF_stop=500e-9
#    wait_F_stop=2e-9
#    wait_FG_stop=0e-9
#    wait_G_stop=0e-9
#    wait_GH_stop=0e-9
#    wait_H_stop=0e-9
#    wait_HI_stop=0e-9
#    wait_I_stop=0e-9
#    wait_IJ_stop=0e-9
#    wait_J_stop=10e-9
##   ##############################

#
#
#    X_A=X_I=X_J=-0.01865*db_atenuation_blue/2;
#    X_B=X_H=-0.02297*db_atenuation_blue/2;
#    X_D=X_F=-0.02487*db_atenuation_blue/2;
#    X_E=-0.004101*db_atenuation_blue/2;
#    X_C=X_G=-0.0527*db_atenuation_blue/2;
#
#
#
#    Y_A=Y_I=Y_J=-0.03065*db_atenuation_black/2;
#    Y_B=Y_H=-0.02703*db_atenuation_black/2;
#    Y_D=Y_F=-0.02535*db_atenuation_black/2;
#    Y_E=-0.04349*db_atenuation_black/2;
#    Y_C=Y_G=-0.001139*db_atenuation_black/2;
#
#
#
#
#
#    wait_A_start=24.98e-6
#    wait_AB_start=0e-9
#    wait_B_start=2e-9
#    wait_BC_start=500e-9
#    wait_C_start=2e-9
#    wait_CD_start=0e-9
#    wait_D_start=1e-9#
#    wait_DE_start=0e-9
#    wait_E_start=1e-9###
#    wait_EF_start=0e-9
#    wait_F_start=0e-9#
#    wait_FG_start=0e-9
#    wait_G_start=2e-9
#    wait_GH_start=500e-9
#    wait_H_start=2e-9
#    wait_HI_start=0e-9
#    wait_I_start=0e-9
#    wait_IJ_start=0e-9
#    wait_J_start=10e-9
#        
#    
#    wait_A_stop=24.98e-6
#    wait_AB_stop=0e-9
#    wait_B_stop=2e-9
#    wait_BC_stop=500e-9
#    wait_C_stop=2e-9
#    wait_CD_stop=0e-9
#    wait_D_stop=1e-9#
#    wait_DE_stop=0e-9
#    wait_E_stop=1e-9###
#    wait_EF_stop=0e-9
#    wait_F_stop=0e-9#
#    wait_FG_stop=0e-9
#    wait_G_stop=2e-9
#    wait_GH_stop=500e-9
#    wait_H_stop=2e-9
#    wait_HI_stop=0e-9
#    wait_I_stop=0e-9
#    wait_IJ_stop=0e-9
#    wait_J_stop=10e-9
#    
#    N_step = 1
#    
########  ###########################
#
#
#    delta_t=-2e-9
#    trigg_amp=-0.0*db_atenuation_red/2;
#    trigg_channel_length=0e-9 
#    C1_DATA,C2_DATA,C3_DATA,C4_DATA,JUMPS_DATA,SIZE,MARKER_C1_1,MARKER_C2_1,MARKER_C3_1,MARKER_C4_1,MARKER_C1_2,MARKER_C2_2,MARKER_C3_2,MARKER_C4_2,AMPLITUDE,OFFSET=multi_rabi_waitingtime(X_A,Y_A,X_B,Y_B, X_C, Y_C,X_D,Y_D,X_E,Y_E,X_F,Y_F,X_G,Y_G,X_H,Y_H,X_I,Y_I,X_J,Y_J,wait_A_start,wait_AB_start,wait_B_start,wait_BC_start, wait_C_start,wait_CD_start,wait_D_start,wait_DE_start,wait_E_start,wait_EF_start,wait_F_start,wait_FG_start,wait_G_start,wait_GH_start,wait_H_start,wait_HI_start,wait_I_start,wait_IJ_start,wait_J_start,wait_A_stop,wait_AB_stop,wait_B_stop,wait_BC_stop,wait_C_stop,wait_CD_stop,wait_D_stop,wait_DE_stop,wait_E_stop,wait_EF_stop,wait_F_stop,wait_FG_stop,wait_G_stop,wait_GH_stop,wait_H_stop,wait_HI_stop,wait_I_stop,wait_IJ_stop,wait_J_stop,N_step,delta_t, trigg_amp, trigg_channel_length)



##################################
#######     amplitude      #######
##################################
#########
#########

###
#    X_A_start=X_I_start=X_J_start=-0.01595*db_atenuation_blue/2;
#    X_B_start=X_H_start=-0.02378*db_atenuation_blue/2;
#    X_D_start=X_F_start=-0.03*db_atenuation_blue/2;
#    X_E_start=-0.01027*db_atenuation_blue/2;
#    X_C_start=X_G_start=-0.04027*db_atenuation_blue/2;
#    
#    X_A_stop=X_I_stop=X_J_stop=-0.01595*db_atenuation_blue/2;
#    X_B_stop=X_H_stop=-0.02378*db_atenuation_blue/2;
#    X_D_stop=X_F_stop=-0.03*db_atenuation_blue/2;
#    X_E_stop=-0.00*db_atenuation_blue/2;
#    X_C_stop=X_G_stop=-0.04027*db_atenuation_blue/2;
#
# 
#    
#    Y_A_start=Y_I_start=Y_J_start=-0.02745*db_atenuation_black/2;
#    Y_B_start=Y_H_start=-0.02104*db_atenuation_black/2;
#    Y_D_start=Y_F_start=-0.02188*db_atenuation_black/2;
#    Y_E_start=-0.03219*db_atenuation_black/2;
#    Y_C_start=Y_G_start=-0.007552*db_atenuation_black/2;
#
#    Y_A_stop=Y_I_stop=Y_J_stop=-0.02745*db_atenuation_black/2;
#    Y_B_stop=Y_H_stop=-0.02104*db_atenuation_black/2;
#    Y_D_stop=Y_F_stop=-0.02188*db_atenuation_black/2;
#    Y_E_stop=-0.04058*db_atenuation_black/2;
#    Y_C_stop=Y_G_stop=-0.007552*db_atenuation_black/2
#        
#    N_step = 200
#
#    wait_A_start=29.98e-6
#    wait_AB_start=0e-9
#    wait_B_start=2e-9
#    wait_BC_start=500e-9
#    wait_C_start=2e-9
#    wait_CD_start=0e-9
#    wait_D_start=0e-9#
#    wait_DE_start=0e-9
#    wait_E_start=1e-9###
#    wait_EF_start=0e-9
#    wait_F_start=0e-9#
#    wait_FG_start=0e-9
#    wait_G_start=2e-9
#    wait_GH_start=500e-9
#    wait_H_start=2e-9
#    wait_HI_start=0e-9
#    wait_I_start=0e-9
#    wait_IJ_start=0e-9
#    wait_J_start=10e-9
#        
#    
#    wait_A_stop=29.98e-6
#    wait_AB_stop=0e-9
#    wait_B_stop=2e-9
#    wait_BC_stop=500e-9
#    wait_C_stop=2e-9
#    wait_CD_stop=0e-9
#    wait_D_stop=0e-9#
#    wait_DE_stop=0e-9
#    wait_E_stop=1e-9###
#    wait_EF_stop=0e-9
#    wait_F_stop=0e-9#
#    wait_FG_stop=0e-9
#    wait_G_stop=2e-9
#    wait_GH_stop=500e-9
#    wait_H_stop=2e-9
#    wait_HI_stop=0e-9
#    wait_I_stop=0e-9
#    wait_IJ_stop=0e-9
#    wait_J_stop=10e-9
#    
#    time = 469
#    
    
#####################################################################
######
#            
    X_A_start=X_B_start=X_C_start=X_D_start=X_E_start=X_F_start=X_H_start=X_I_start=X_J_start=-0.02243*db_atenuation_blue/2;
    X_G_start=-0.05784*db_atenuation_blue/2;

    
    X_A_stop=X_B_stop=X_C_stop=X_D_stop=X_E_stop=X_F_stop=X_H_stop=X_I_stop=X_J_stop=-0.01324*db_atenuation_blue/2;
    X_G_stop=-0.05784*db_atenuation_blue/2;    
    
    
    
    
    Y_A_start=Y_B_start=Y_C_start=Y_D_start=Y_E_start=Y_F_start=Y_H_start=Y_I_start=Y_J_start=-0.02955*db_atenuation_black/2;
    Y_G_start=-0.0*db_atenuation_black/2;
#    
    
    Y_A_stop=Y_B_stop=Y_C_stop=Y_D_stop=Y_E_stop=Y_F_stop=Y_H_stop=Y_I_stop=Y_J_stop=-0.03686*db_atenuation_black/2;
    Y_G_stop=-0.0*db_atenuation_black/2;#
    
    


    N_step = 200
    time = 100
##
##
    wait_A_start=29.9e-6;
    wait_AB_start=0e-6;
    wait_B_start=0e-6;#
    wait_BC_start=0e-6;
    wait_C_start=0e-6;
    wait_CD_start=0e-9;
    wait_D_start=0e-9;
    wait_DE_start=0e-9;
    wait_E_start=0e-9;
    wait_EF_start=0e-9;
    wait_F_start=0e-9;
    wait_FG_start=0e-9;
    wait_G_start=0.1e-6;###
    wait_GH_start=0e-9;
    wait_H_start=0e-6;
    wait_HI_start=0e-9
    wait_I_start=1e-9
    wait_IJ_start=0e-9
    wait_J_start=370e-6
     
    wait_A_stop=29.9e-6;
    wait_AB_stop=0e-6;
    wait_B_stop=0e-6;#
    wait_BC_stop=0e-6;
    wait_C_stop=0e-6;
    wait_CD_stop=0e-6;
    wait_D_stop=0e-9;
    wait_DE_stop=0e-6;
    wait_E_stop=0e-9;
    wait_EF_stop=0e-6;
    wait_F_stop=0e-9;
    wait_FG_stop=0e-6;
    wait_G_stop=0.1e-6;###
    wait_GH_stop=0e-6;
    wait_H_stop=0;
    wait_HI_stop=0e-9
    wait_I_stop=1e-9
    wait_IJ_stop=0e-9
    wait_J_stop=370e-6
###    
#####################################################################

#####################################################################
#
#

#    X_A_start=X_I_start=X_J_start=-0.02054*db_atenuation_blue/2;
#    X_B_start=X_H_start=-0.02703*db_atenuation_blue/2;
#    X_D_start=X_F_start=-0.03*db_atenuation_blue/2;
#    X_E_start=-0.00554*db_atenuation_blue/2;
#    X_C_start=X_G_start=-0.04595*db_atenuation_blue/2;
#    
#    X_A_stop=X_I_stop=X_J_stop=-0.02054*db_atenuation_blue/2;
#    X_B_stop=X_H_stop=-0.02703*db_atenuation_blue/2;
#    X_D_stop=X_F_stop=-0.03*db_atenuation_blue/2;
#    X_E_stop=-0.00554*db_atenuation_blue/2;
#    X_C_stop=X_G_stop=-0.04595*db_atenuation_blue/2;
#
# 
#    
#    Y_A_start=Y_I_start=Y_J_start=-0.02511*db_atenuation_black/2;
#    Y_B_start=Y_H_start=-0.01984*db_atenuation_black/2;
#    Y_D_start=Y_F_start=-0.02188*db_atenuation_black/2;
#    Y_E_start=-0.03717*db_atenuation_black/2;
#    Y_C_start=Y_G_start=-0.004615*db_atenuation_black/2;
#
#    Y_A_stop=Y_I_stop=Y_J_stop=-0.02511*db_atenuation_black/2;
#    Y_B_stop=Y_H_stop=-0.01984*db_atenuation_black/2;
#    Y_D_stop=Y_F_stop=-0.02188*db_atenuation_black/2;
#    Y_E_stop=-0.03717*db_atenuation_black/2;
#    Y_C_stop=Y_G_stop=-0.004615*db_atenuation_black/2
#
#
#    N_step = 20
#
#     
#    wait_A_start=29.98e-6
#    wait_AB_start=0e-9
#    wait_B_start=2e-9
#    wait_BC_start=500e-9
#    wait_C_start=2e-9
#    wait_CD_start=0e-9
#    wait_D_start=0e-9#
#    wait_DE_start=0e-9
#    wait_E_start=1e-9###
#    wait_EF_start=0e-9
#    wait_F_start=0e-9#
#    wait_FG_start=0e-9
#    wait_G_start=2e-9
#    wait_GH_start=500e-9
#    wait_H_start=2e-9
#    wait_HI_start=0e-9
#    wait_I_start=0e-9
#    wait_IJ_start=0e-9
#    wait_J_start=10e-9
#        
#    
#    wait_A_stop=29.98e-6
#    wait_AB_stop=0e-9
#    wait_B_stop=2e-9
#    wait_BC_stop=500e-9
#    wait_C_stop=2e-9
#    wait_CD_stop=0e-9
#    wait_D_stop=0e-9#
#    wait_DE_stop=0e-9
#    wait_E_stop=1e-9###
#    wait_EF_stop=0e-9
#    wait_F_stop=0e-9#
#    wait_FG_stop=0e-9
#    wait_G_stop=2e-9
#    wait_GH_stop=500e-9
#    wait_H_stop=2e-9
#    wait_HI_stop=0e-9
#    wait_I_stop=0e-9
#    wait_IJ_stop=0e-9
#    wait_J_stop=10e-9
#    
#    time = 469
##    

###################################################################

    delta_t=-2e-9
    trigg_amp_init=0.0*db_atenuation_red/2;
    trigg_amp_end=-0.0*db_atenuation_red/2;
    trigg_channel_length=6e-9  
    C1_DATA,C2_DATA,C3_DATA,C4_DATA,JUMPS_DATA,SIZE,MARKER_C1_1,MARKER_C2_1,MARKER_C3_1,MARKER_C4_1,MARKER_C1_2,MARKER_C2_2,MARKER_C3_2,MARKER_C4_2,AMPLITUDE,OFFSET=multi_rabi_amplitude(X_A_start,Y_A_start,X_B_start,Y_B_start, X_C_start, Y_C_start,X_D_start,Y_D_start,X_E_start,Y_E_start,X_F_start,Y_F_start,X_G_start,Y_G_start,X_H_start,Y_H_start,X_I_start,Y_I_start,X_J_start,Y_J_start,X_A_stop,Y_A_stop,X_B_stop,Y_B_stop, X_C_stop, Y_C_stop,X_D_stop,Y_D_stop,X_E_stop,Y_E_stop,X_F_stop,Y_F_stop,X_G_stop,Y_G_stop,X_H_stop,Y_H_stop,X_I_stop,Y_I_stop,X_J_stop,Y_J_stop,wait_A_start,wait_AB_start,wait_B_start,wait_BC_start, wait_C_start,wait_CD_start,wait_D_start,wait_DE_start,wait_E_start,wait_EF_start,wait_F_start,wait_FG_start,wait_G_start,wait_GH_start,wait_H_start,wait_HI_start,wait_I_start,wait_IJ_start,wait_J_start,wait_A_stop,wait_AB_stop,wait_B_stop,wait_BC_stop,wait_C_stop,wait_CD_stop,wait_D_stop,wait_DE_stop,wait_E_stop,wait_EF_stop,wait_F_stop,wait_FG_stop,wait_G_stop,wait_GH_stop,wait_H_stop,wait_HI_stop,wait_I_stop,wait_IJ_stop,wait_J_stop,N_step,delta_t, trigg_amp_init,trigg_amp_end, trigg_channel_length)

####################################################################
#    print MARKER_C4_1
    for i in range(1,N_step+1):
#
        plt.figure(2)
        plt.plot(C1_DATA[i][:])
#        plt.plot(C2_DATA[i][:])
#        plt.plot(C3_DATA[i][:]+0.5)
#        plt.plot(C4_DATA[i][:])
        plt.plot(MARKER_C4_2[i][:]-0.5)
        plt.plot(MARKER_C4_1[i][:]+0.75)

#



    AWG_SR = 1e7
    ADC_SR = 1e6
    
    C1_value = C1_DATA[1][-1]
    C2_value = C2_DATA[1][-1]
    C3_value = C3_DATA[1][-1]
    C4_value = C4_DATA[1][-1]


    default_value =0
    
    C1_DATA_WAIT,C2_DATA_WAIT,C3_DATA_WAIT,C4_DATA_WAIT,MARKER_C1_1_WAIT,MARKER_C2_1_WAIT,MARKER_C3_1_WAIT,MARKER_C4_1_WAIT,MARKER_C1_2_WAIT,MARKER_C2_2_WAIT,MARKER_C3_2_WAIT,MARKER_C4_2_WAIT,OFFSET_WAIT,SIZE_WAIT,time=wait(time,AWG_SR,ADC_SR,C1_value,C2_value, default_value)




    print 'Did you change the renormalisation ?'
    if raw_input()=='Y':
        print('Do you want to send the waveforms Y/N ?')
        if raw_input()=='Y':
            SendWaveForm(N_step)

    del C1_DATA
    del C2_DATA
    del C3_DATA
    del C4_DATA
    del SIZE
    del MARKER_C1_1
    del MARKER_C2_1
    del MARKER_C3_1
    del MARKER_C4_1
    del MARKER_C1_2
    del MARKER_C2_2
    del MARKER_C3_2
    del MARKER_C4_2
    del C1_DATA_WAIT
    del C2_DATA_WAIT
    del C3_DATA_WAIT
    del C4_DATA_WAIT
    del MARKER_C1_1_WAIT
    del MARKER_C2_1_WAIT
    del MARKER_C3_1_WAIT
    del MARKER_C4_1_WAIT
    del MARKER_C1_2_WAIT
    del MARKER_C2_2_WAIT
    del MARKER_C3_2_WAIT
    del MARKER_C4_2_WAIT