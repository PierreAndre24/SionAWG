# -*- coding: utf-8 -*-
"""
Created on Mon May 04 16:14:40 2015

@author: vivien.thiney
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



def rabi(X_A,Y_A,X_B,Y_B,X_C,Y_C,X_D,Y_D,X_E,Y_E,X_F,Y_F,X_G,Y_G,X_H,Y_H,X_I,Y_I,X_J,Y_J,wait_A,wait_AB,wait_B,wait_BC,wait_C,wait_CD,wait_D,wait_DE,wait_E,wait_EF,wait_F,wait_FG,wait_G,wait_GH,wait_H,wait_HI,wait_I,wait_IJ,wait_J,secure_prep_length,delta_t, trigg_amp, trigg_channel_length):

    deltaX_AB=X_B-X_A
    deltaX_BC=X_C-X_B
    deltaX_CD=X_D-X_C
    deltaX_DE=X_E-X_D
    deltaX_EF=X_F-X_E
    deltaX_FG=X_G-X_F
    deltaX_GH=X_H-X_G
    deltaX_HI=X_I-X_H
    deltaX_IJ=X_J-X_I


    deltaY_AB=Y_B-Y_A
    deltaY_BC=Y_C-Y_B
    deltaY_CD=Y_D-Y_C
    deltaY_DE=Y_E-Y_D
    deltaY_EF=Y_F-Y_E
    deltaY_FG=Y_G-Y_F
    deltaY_GH=Y_H-Y_G
    deltaY_HI=Y_I-Y_H
    deltaY_IJ=Y_J-Y_I


    ADC_samplingrate = 1.0e6;
    
    
    AWG_samplingrate = 1.0e7;
#    AWG_samplingrate = 1.0e9;
#   
   
    
    trigg_length = 1* AWG_samplingrate/ADC_samplingrate;   # change the sampling rate of the AWG in number of point related to the sampling rate of the ADC
    Nindex = 2;   # number of sequence played by the AWG. The first stay at zero (protect the gates), the second is the one that we want to play
    trigg_period = 1*trigg_length   # define the period of a trigg, related to the triggering of the ADC. With ADC trigg period=2*trigglength (one up and one down). With the LeCroy trigg period =1trigg length (just say to the LeCroy when it starts to measure, can do the same with the ADC)
# ##   trigg_length=1µs


    secure_prep_length=0; #length to go to the initial value or to 0 safely
    checking_triggers=28*trigg_length;  #number of points(=time in µs) measured in the initialisation step, has to be smaller than the initialisation time



   ####     convert the time in second to a certain number of point for the AWG
   
    wait_A  = np.around(wait_A  * ADC_samplingrate * trigg_period);   
    wait_B  = np.around(wait_B  * ADC_samplingrate * trigg_period);
    wait_C  = np.around(wait_C  * ADC_samplingrate * trigg_period);
    wait_D  = np.around(wait_D  * ADC_samplingrate * trigg_period);
    wait_E  = np.around(wait_E  * ADC_samplingrate * trigg_period);
    wait_F  = np.around(wait_F  * ADC_samplingrate * trigg_period);    
    wait_G  = np.around(wait_G  * ADC_samplingrate * trigg_period);
    wait_H  = np.around(wait_H  * ADC_samplingrate * trigg_period);
    wait_I  = np.around(wait_I  * ADC_samplingrate * trigg_period);
    wait_J  = np.around(wait_J  * ADC_samplingrate * trigg_period);
    
    wait_AB = np.around(wait_AB * ADC_samplingrate * trigg_period);
    wait_BC = np.around(wait_BC * ADC_samplingrate * trigg_period);
    wait_CD = np.around(wait_CD * ADC_samplingrate * trigg_period);
    wait_DE = np.around(wait_DE * ADC_samplingrate * trigg_period);
    wait_EF = np.around(wait_EF * ADC_samplingrate * trigg_period);
    wait_FG = np.around(wait_FG * ADC_samplingrate * trigg_period);
    wait_GH = np.around(wait_GH * ADC_samplingrate * trigg_period);
    wait_HI = np.around(wait_HI * ADC_samplingrate * trigg_period);
    wait_IJ = np.around(wait_IJ * ADC_samplingrate * trigg_period);
    
    trigg_channel_length= np.around(trigg_channel_length * ADC_samplingrate * trigg_period);  
    delta_t= np.around(delta_t * ADC_samplingrate * trigg_period);


#####
##     parameters for the triggering of the RF signal
####
    start_RF=-secure_prep_length/2; #here start the RF only for C&D (secure_prep_length+start_RF)
    stop_RF = 0; # here stop the RF during the secure_prep_length
    Switch_RF_on = 1; #lvl on of the RF switch
    Switch_RF_off= 0;
#####
    

    scan_length= (wait_A+wait_B+wait_C+wait_D+wait_E+wait_F+wait_G+wait_AB+wait_BC+wait_CD+wait_DE+wait_EF+wait_FG+wait_GH+wait_H+wait_HI+wait_I+wait_IJ+wait_J) + 2*secure_prep_length;#length of a complete scan, with the ramp, steps, security ramp, etc
#
#

    ########################################
    #       INITIALISATION
    ########################################


    C1_DATA=np.zeros((Nindex,scan_length));
    C2_DATA=np.zeros((Nindex,scan_length));
    C3_DATA=np.zeros((Nindex,scan_length));
    C4_DATA=np.zeros((Nindex,scan_length));

    MARKER_C1_1=np.zeros((Nindex,scan_length));
    MARKER_C2_1=np.zeros((Nindex,scan_length));
    MARKER_C3_1=np.zeros((Nindex,scan_length));
    MARKER_C4_1=np.zeros((Nindex,scan_length));

    MARKER_C1_2=np.zeros((Nindex,scan_length));
    MARKER_C2_2=np.zeros((Nindex,scan_length));
    MARKER_C3_2=np.zeros((Nindex,scan_length));
    MARKER_C4_2=np.zeros((Nindex,scan_length));

    JUMPS_DATA=np.zeros((Nindex,4));
    SIZE=scan_length;


    ########################################
    #          JUMP CHANNEL 1&2
    ########################################


    #initialisation of the table
    AX=np.zeros((1,wait_A+wait_B+wait_C+wait_D+wait_E+wait_F+wait_G+wait_H+wait_I+wait_J+wait_AB+wait_BC+wait_CD+wait_DE+wait_EF+wait_FG+wait_GH+wait_HI+wait_IJ))  
    
    AX[0][0:wait_A] = np.ones((1,wait_A))*X_A;
    if wait_AB>0.:
        AX[0][wait_A:wait_A+wait_AB]=np.arange(X_A,X_B+deltaX_AB/wait_AB,deltaX_AB/(wait_AB-1));
    AX[0][wait_A+wait_AB:wait_A+wait_AB+wait_B] = np.ones((1,wait_B))*X_B;
    if wait_BC>0:
        AX[0][wait_A+wait_AB+wait_B:wait_A+wait_AB+wait_B+wait_BC]=np.arange(X_B,X_C+deltaX_BC/wait_BC,deltaX_BC/(wait_BC-1))
    AX[0][wait_A+wait_AB+wait_B+wait_BC:wait_A+wait_AB+wait_B+wait_BC+wait_C]=np.ones((1,wait_C))*X_C
    if wait_CD>0:
        AX[0][wait_A+wait_AB+wait_B+wait_BC+wait_C:wait_A+wait_AB+wait_B+wait_BC+wait_C+wait_CD]=np.arange(X_C,X_D+deltaX_CD/wait_CD,deltaX_CD/(wait_CD-1))
    AX[0][wait_A+wait_AB+wait_B+wait_BC+wait_C+wait_CD:wait_A+wait_AB+wait_B+wait_BC+wait_C+wait_CD+wait_D]=np.ones((1,wait_D))*X_D;
    if wait_DE>0:
        AX[0][wait_A+wait_AB+wait_B+wait_BC+wait_C+wait_CD+wait_D:wait_A+wait_AB+wait_B+wait_BC+wait_C+wait_CD+wait_D+wait_DE]=np.arange(X_D,X_E+deltaX_DE/wait_DE,deltaX_DE/(wait_DE-1))
    AX[0][wait_A+wait_AB+wait_B+wait_BC+wait_C+wait_CD+wait_D+wait_DE:wait_A+wait_AB+wait_B+wait_BC+wait_C+wait_CD+wait_D+wait_DE+wait_E]=np.ones((1,wait_E))*X_E;
   
    if wait_EF>0:
        AX[0][wait_A+wait_AB+wait_B+wait_BC+wait_C+wait_CD+wait_D+wait_DE+wait_E:wait_A+wait_AB+wait_B+wait_BC+wait_C+wait_CD+wait_D+wait_DE+wait_E+wait_EF]=np.arange(X_E,X_F+deltaX_EF/wait_EF,deltaX_EF/(wait_EF-1))
    AX[0][wait_A+wait_AB+wait_B+wait_BC+wait_C+wait_CD+wait_D+wait_DE+wait_E+wait_EF:wait_A+wait_AB+wait_B+wait_BC+wait_C+wait_CD+wait_D+wait_DE+wait_E+wait_EF+wait_F]=np.ones((1,wait_F))*X_F;
    
    if wait_FG>0:
        AX[0][wait_A+wait_AB+wait_B+wait_BC+wait_C+wait_CD+wait_D+wait_DE+wait_E+wait_EF+wait_F:wait_A+wait_AB+wait_B+wait_BC+wait_C+wait_CD+wait_D+wait_DE+wait_E+wait_EF+wait_F+wait_FG]=np.arange(X_F,X_G+deltaX_FG/wait_FG,deltaX_FG/(wait_FG-1))
    AX[0][wait_A+wait_AB+wait_B+wait_BC+wait_C+wait_CD+wait_D+wait_DE+wait_E+wait_EF+wait_F+wait_FG:wait_A+wait_AB+wait_B+wait_BC+wait_C+wait_CD+wait_D+wait_DE+wait_E+wait_EF+wait_F+wait_FG+wait_G]=np.ones((1,wait_G))*X_G;

    if wait_GH>0:
        AX[0][wait_A+wait_AB+wait_B+wait_BC+wait_C+wait_CD+wait_D+wait_DE+wait_E+wait_EF+wait_F+wait_FG+wait_G:wait_A+wait_AB+wait_B+wait_BC+wait_C+wait_CD+wait_D+wait_DE+wait_E+wait_EF+wait_F+wait_FG+wait_GH+wait_G]=np.arange(X_G,X_H+deltaX_GH/wait_GH,deltaX_GH/(wait_GH-1))
    AX[0][wait_A+wait_AB+wait_B+wait_BC+wait_C+wait_CD+wait_D+wait_DE+wait_E+wait_EF+wait_F+wait_FG+wait_G+wait_GH:wait_A+wait_AB+wait_B+wait_BC+wait_C+wait_CD+wait_D+wait_DE+wait_E+wait_EF+wait_F+wait_FG+wait_G+wait_GH+wait_H]=np.ones((1,wait_H))*X_H;

    if wait_HI>0:
        AX[0][wait_A+wait_AB+wait_B+wait_BC+wait_C+wait_CD+wait_D+wait_DE+wait_E+wait_EF+wait_F+wait_FG+wait_G+wait_GH+wait_H:wait_A+wait_AB+wait_B+wait_BC+wait_C+wait_CD+wait_D+wait_DE+wait_E+wait_EF+wait_F+wait_FG+wait_G+wait_GH+wait_H+wait_HI]=np.linspace(X_H,X_I,wait_HI)
    AX[0][wait_A+wait_AB+wait_B+wait_BC+wait_C+wait_CD+wait_D+wait_DE+wait_E+wait_EF+wait_F+wait_FG+wait_G+wait_GH+wait_H+wait_HI:wait_A+wait_AB+wait_B+wait_BC+wait_C+wait_CD+wait_D+wait_DE+wait_E+wait_EF+wait_F+wait_FG+wait_G+wait_GH+wait_H+wait_HI+wait_I]=np.ones((1,wait_I))*X_I;

    if wait_IJ>0:
        AX[0][wait_A+wait_AB+wait_B+wait_BC+wait_C+wait_CD+wait_D+wait_DE+wait_E+wait_EF+wait_F+wait_FG+wait_G+wait_GH+wait_H+wait_HI+wait_I:wait_A+wait_AB+wait_B+wait_BC+wait_C+wait_CD+wait_D+wait_DE+wait_E+wait_EF+wait_F+wait_FG+wait_G+wait_GH+wait_H+wait_HI+wait_I+wait_IJ]=np.linspace(X_I,X_J,wait_IJ)
    AX[0][wait_A+wait_AB+wait_B+wait_BC+wait_C+wait_CD+wait_D+wait_DE+wait_E+wait_EF+wait_F+wait_FG+wait_G+wait_GH+wait_H+wait_HI+wait_I+wait_IJ:wait_A+wait_AB+wait_B+wait_BC+wait_C+wait_CD+wait_D+wait_DE+wait_E+wait_EF+wait_F+wait_FG+wait_G+wait_GH+wait_H+wait_HI+wait_I+wait_IJ+wait_J]=np.ones((1,wait_J))*X_J;



#############################################


    #initialisation of the table
    AY=np.zeros((1,wait_A+wait_B+wait_C+wait_D+wait_E+wait_F+wait_G+wait_H+wait_I+wait_J+wait_AB+wait_BC+wait_CD+wait_DE+wait_EF+wait_FG+wait_GH+wait_HI+wait_IJ))  

 
    AY[0][0:wait_A] = np.ones((1,wait_A))*Y_A;
    if wait_AB>0.:
        AY[0][wait_A:wait_A+wait_AB]=np.arange(Y_A,Y_B+deltaY_AB/wait_AB,deltaY_AB/(wait_AB-1));
    AY[0][wait_A+wait_AB:wait_A+wait_AB+wait_B] = np.ones((1,wait_B))*Y_B;
    if wait_BC>0:
        AY[0][wait_A+wait_AB+wait_B:wait_A+wait_AB+wait_B+wait_BC]=np.arange(Y_B,Y_C+deltaY_BC/wait_BC,deltaY_BC/(wait_BC-1))
    AY[0][wait_A+wait_AB+wait_B+wait_BC:wait_A+wait_AB+wait_B+wait_BC+wait_C]=np.ones((1,wait_C))*Y_C
    if wait_CD>0:
        AY[0][wait_A+wait_AB+wait_B+wait_BC+wait_C:wait_A+wait_AB+wait_B+wait_BC+wait_C+wait_CD]=np.arange(Y_C,Y_D+deltaY_CD/wait_CD,deltaY_CD/(wait_CD-1))
    AY[0][wait_A+wait_AB+wait_B+wait_BC+wait_C+wait_CD:wait_A+wait_AB+wait_B+wait_BC+wait_C+wait_CD+wait_D]=np.ones((1,wait_D))*Y_D;
    if wait_DE>0:
        AY[0][wait_A+wait_AB+wait_B+wait_BC+wait_C+wait_CD+wait_D:wait_A+wait_AB+wait_B+wait_BC+wait_C+wait_CD+wait_D+wait_DE]=np.arange(Y_D,Y_E+deltaY_DE/wait_DE,deltaY_DE/(wait_DE-1))
    AY[0][wait_A+wait_AB+wait_B+wait_BC+wait_C+wait_CD+wait_D+wait_DE:wait_A+wait_AB+wait_B+wait_BC+wait_C+wait_CD+wait_D+wait_DE+wait_E]=np.ones((1,wait_E))*Y_E;

    if wait_EF>0:
        AY[0][wait_A+wait_AB+wait_B+wait_BC+wait_C+wait_CD+wait_D+wait_DE+wait_E:wait_A+wait_AB+wait_B+wait_BC+wait_C+wait_CD+wait_D+wait_DE+wait_E+wait_EF]=np.arange(Y_E,Y_F+deltaY_EF/wait_EF,deltaY_EF/(wait_EF-1))
    AY[0][wait_A+wait_AB+wait_B+wait_BC+wait_C+wait_CD+wait_D+wait_DE+wait_E+wait_EF:wait_A+wait_AB+wait_B+wait_BC+wait_C+wait_CD+wait_D+wait_DE+wait_E+wait_EF+wait_F]=np.ones((1,wait_F))*Y_F;
    if wait_FG>0:
        AY[0][wait_A+wait_AB+wait_B+wait_BC+wait_C+wait_CD+wait_D+wait_DE+wait_E+wait_EF+wait_F:wait_A+wait_AB+wait_B+wait_BC+wait_C+wait_CD+wait_D+wait_DE+wait_E+wait_EF+wait_F+wait_FG]=np.arange(Y_F,Y_G+deltaY_FG/wait_FG,deltaY_FG/(wait_FG-1))
    AY[0][wait_A+wait_AB+wait_B+wait_BC+wait_C+wait_CD+wait_D+wait_DE+wait_E+wait_EF+wait_F+wait_FG:wait_A+wait_AB+wait_B+wait_BC+wait_C+wait_CD+wait_D+wait_DE+wait_E+wait_EF+wait_F+wait_FG+wait_G]=np.ones((1,wait_G))*Y_G;
    
    if wait_GH>0:
        AY[0][wait_A+wait_AB+wait_B+wait_BC+wait_C+wait_CD+wait_D+wait_DE+wait_E+wait_EF+wait_F+wait_FG+wait_G:wait_A+wait_AB+wait_B+wait_BC+wait_C+wait_CD+wait_D+wait_DE+wait_E+wait_EF+wait_F+wait_FG+wait_G+wait_GH]=np.arange(Y_G,Y_H+deltaY_GH/wait_GH,deltaY_GH/(wait_GH-1))
    AY[0][wait_A+wait_AB+wait_B+wait_BC+wait_C+wait_CD+wait_D+wait_DE+wait_E+wait_EF+wait_F+wait_FG+wait_G+wait_GH:wait_A+wait_AB+wait_B+wait_BC+wait_C+wait_CD+wait_D+wait_DE+wait_E+wait_EF+wait_F+wait_FG+wait_G+wait_GH+wait_H]=np.ones((1,wait_H))*Y_H;

    if wait_HI>0:
        AY[0][wait_A+wait_AB+wait_B+wait_BC+wait_C+wait_CD+wait_D+wait_DE+wait_E+wait_EF+wait_F+wait_FG+wait_G+wait_GH+wait_H:wait_A+wait_AB+wait_B+wait_BC+wait_C+wait_CD+wait_D+wait_DE+wait_E+wait_EF+wait_F+wait_FG+wait_G+wait_GH+wait_H+wait_HI]=np.linspace(Y_H,Y_I,wait_HI)
    AY[0][wait_A+wait_AB+wait_B+wait_BC+wait_C+wait_CD+wait_D+wait_DE+wait_E+wait_EF+wait_F+wait_FG+wait_G+wait_GH+wait_H+wait_HI:wait_A+wait_AB+wait_B+wait_BC+wait_C+wait_CD+wait_D+wait_DE+wait_E+wait_EF+wait_F+wait_FG+wait_G+wait_GH+wait_H+wait_HI+wait_I]=np.ones((1,wait_I))*Y_I;

    if wait_IJ>0:
        AY[0][wait_A+wait_AB+wait_B+wait_BC+wait_C+wait_CD+wait_D+wait_DE+wait_E+wait_EF+wait_F+wait_FG+wait_G+wait_GH+wait_H+wait_HI+wait_I:wait_A+wait_AB+wait_B+wait_BC+wait_C+wait_CD+wait_D+wait_DE+wait_E+wait_EF+wait_F+wait_FG+wait_G+wait_GH+wait_H+wait_HI+wait_I+wait_IJ]=np.linspace(Y_I,Y_J,wait_IJ)
    AY[0][wait_A+wait_AB+wait_B+wait_BC+wait_C+wait_CD+wait_D+wait_DE+wait_E+wait_EF+wait_F+wait_FG+wait_G+wait_GH+wait_H+wait_HI+wait_I+wait_IJ:wait_A+wait_AB+wait_B+wait_BC+wait_C+wait_CD+wait_D+wait_DE+wait_E+wait_EF+wait_F+wait_FG+wait_G+wait_GH+wait_H+wait_HI+wait_I+wait_IJ+wait_J]=np.ones((1,wait_J))*Y_J;



    C2_DATA[1] = AX
    C1_DATA[1] = AY


    

    #######################################
    #                   TRIGGERS
    ########################################

####    triggers for the measure
 ####################the trigger is positioned at wait_D - checking_triggers. So the measurement will cover checking_triggers+wait_DE+wait_E


    MARKER = np.zeros((scan_length));
    MARKER[secure_prep_length+wait_A+wait_AB+wait_B+wait_BC+wait_C+wait_CD+wait_D+wait_DE+wait_E+wait_EF+wait_F+wait_FG+wait_G+wait_GH+wait_H+wait_HI+wait_I+wait_IJ-checking_triggers-trigg_length:secure_prep_length+wait_A+wait_AB+wait_B+wait_BC+wait_C+wait_CD+wait_D+wait_DE+wait_E+wait_EF+wait_F+wait_FG+wait_G+wait_GH+wait_H+wait_HI+wait_I+wait_IJ-checking_triggers]=np.ones((1*trigg_length));    
#    MARKER[0:trigg_length]=np.ones((1*trigg_length));  
#    MARKER_C1_1[1] = MARKER;
    MARKER_C4_2[1] = MARKER;

    
    
#### trigger/pulse on the others channel  
    TRIGG_CHANNEL=np.zeros((scan_length))
    
    ####  step
    TRIGG_CHANNEL[secure_prep_length+wait_A+wait_AB+wait_B+wait_BC+wait_C+wait_CD+wait_D+wait_DE+delta_t:secure_prep_length+trigg_channel_length+wait_A+wait_AB+wait_B+wait_BC+wait_C+wait_CD+wait_D+wait_DE+delta_t]=np.ones((trigg_channel_length))*trigg_amp 
    
    ####  ramp
#    TRIGG_CHANNEL[secure_prep_length+wait_A+wait_AB+wait_B+wait_BC+wait_C+wait_CD+wait_D+wait_DE+delta_t:secure_prep_length+trigg_channel_length+wait_A+wait_AB+wait_B+wait_BC+wait_C+wait_CD+wait_D+wait_DE+delta_t]=np.linspace(0,trigg_amp,trigg_channel_length)


    #### Romain's way
    # two steps of different amplitude

#    trigg_mid=np.ones((trigg_channel_length/2))*trigg_amp/3
#    trigg_top=np.ones((trigg_channel_length/2))*trigg_amp
###    trigg_top=np.linspace(trigg_amp/3,trigg_amp,trigg_channel_length/2)
####    trigg=np.append(trigg_mid,[trigg_top])
####    trigg=np.append(trigg,[trigg_mid])
#    trigg=np.zeros((trigg_channel_length))
#    trigg[0:trigg_channel_length/2]=trigg_mid
#    trigg[trigg_channel_length/2:] =trigg_top
#####    trigg[0:3*trigg_channel_length/8]=np.ones((3*trigg_channel_length/8))*trigg_amp/3
#####    trigg[3*trigg_channel_length/8:3*trigg_channel_length/8+trigg_channel_length/4]=np.ones((trigg_channel_length/4))*trigg_amp
#####    trigg[3*trigg_channel_length/8+trigg_channel_length/4:]=np.ones((3*trigg_channel_length/8))*trigg_amp/3
#    TRIGG_CHANNEL[secure_prep_length+wait_A+wait_AB+wait_B+wait_BC+wait_C+wait_CD+wait_D+wait_DE+delta_t:secure_prep_length+trigg_channel_length+wait_A+wait_AB+wait_B+wait_BC+wait_C+wait_CD+wait_D+wait_DE+delta_t]=trigg


    #### ramp&step
    #### ramp for the trigg_channel_length-1ns at 2/3 of the trigg amplitude then pulse for 1ns of the remaining amp 
#
#    trigg_ramp=np.linspace(0,2*trigg_amp/3,trigg_channel_length-10*trigg_length*ADC_samplingrate/AWG_samplingrate)
#    trigg_step=np.ones((10*trigg_length*ADC_samplingrate/AWG_samplingrate))*trigg_amp/3.
#    trigg=np.zeros((trigg_channel_length))
#    trigg[0:trigg_channel_length-10*trigg_length*ADC_samplingrate/AWG_samplingrate]=trigg_ramp
#    trigg[trigg_channel_length-10*trigg_length*ADC_samplingrate/AWG_samplingrate:]=trigg_step
#    TRIGG_CHANNEL[secure_prep_length+wait_A+wait_AB+wait_B+wait_BC+wait_C+wait_CD-trigg_channel_length-delta_t:secure_prep_length+wait_A+wait_AB+wait_B+wait_BC+wait_C+wait_CD-delta_t]=trigg

#
#
#

#    C3_DATA[1] = TRIGG_CHANNEL;
    C4_DATA[1] = TRIGG_CHANNEL;
#    plt.figure(1)
#    plt.plot(TRIGG_CHANNEL)
##    
###    
    


    ########################################
    #         SWITCH  RF signal
    ########################################


#    Switch_up = np.ones((trigg_length));
    Switch_onoff=np.zeros((scan_length));
#    Switch_onoff[int(wait_G*0.9)+wait_GH+wait_H+wait_HI+wait_I+wait_IJ+wait_J]
    Switch_onoff[secure_prep_length+wait_A+wait_AB+wait_B+wait_BC+wait_C+wait_CD+wait_D+wait_DE+wait_E+wait_EF+wait_F+wait_FG+int(wait_G*0.1):]=0

    MARKER_C4_1[1] = Switch_onoff;
    
#    plt.figure(3)
#    plt.plot(MARKER_C4_1)
#    plt.ylim(-0.5,1.5)
    

######################################################

    # PRECISE THE LENGTH OF EACH INDEX OF YOUR SEQUENCE
    SIZE=np.zeros((1,2));
    SIZE[0][0]=np.shape(C4_DATA)[1];
    SIZE[0][1]=np.shape(C4_DATA)[1];
    #     CONSTRUCTING ARRAY CONTAINING JUMPS/TRIGGERING DATA
    JUMPS_DATA[0,0]=0;      #% "wait"
    JUMPS_DATA[0,1]=0;     # % "repeat"
    JUMPS_DATA[0,2]=2;     # % "event jump to"
    JUMPS_DATA[0,3]=0;     # % "go to"

    JUMPS_DATA[1,0]=0;       # % "wait"
    JUMPS_DATA[1,1]=0;       # % "repeat"
    JUMPS_DATA[1,2]=1;       # % "event jump to"
    JUMPS_DATA[1,3]=0;       # % "go to"


    JUMPS_DATA[-1,3]=1; #% to loop




    # AUTOMATICALLY RETRIEVES THE CHANNEL HIGH/LOW AMPLITUDE/OFFSET VALUES

    HIGHEST = array([C1_DATA.max(),C2_DATA.max(),C3_DATA.max(),C4_DATA.max()]);
    LOWEST  =array([C1_DATA.min(),C2_DATA.min(),C3_DATA.min(),C4_DATA.min()]);
    AMPLITUDE=np.zeros((1,4));
    for i in range(0,3):
        AMPLITUDE[0][i]=2*max(HIGHEST[i]-LOWEST[i],0.02)
    OFFSET = [0,0,0,0];

    # NORMALIZATION OF THE DATA TO BE TRANSMITTED TO THE AWG
#
#    C1_DATA=2*(C1_DATA-OFFSET[0])/AMPLITUDE[0][0];
#    C2_DATA=2*(C2_DATA-OFFSET[1])/AMPLITUDE[0][1];
#    C3_DATA=2*(C3_DATA-OFFSET[2])/AMPLITUDE[0][2];
#    C4_DATA=2*(C4_DATA-OFFSET[3])/AMPLITUDE[0][3];
#


    return C1_DATA,C2_DATA,C3_DATA,C4_DATA,JUMPS_DATA,SIZE,MARKER_C1_1,MARKER_C2_1,MARKER_C3_1,MARKER_C4_1,MARKER_C1_2,MARKER_C2_2,MARKER_C3_2,MARKER_C4_2,AMPLITUDE,OFFSET

