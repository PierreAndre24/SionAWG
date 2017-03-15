# -*- coding: utf-8 -*-
"""
Created on Mon Apr 11 09:38:42 2016

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
from jump import jump
from sweep_n_step2 import sweep_n_step2
from rabi import rabi
from multi_rabi_waitingtime import multi_rabi_waitingtime
from multi_rabi_amplitude import multi_rabi_amplitude



#def multi_amp_wait(X_A_start1,Y_A_start1,X_B_start1,Y_B_start1, X_C_start1, Y_C_start1,X_D_start1,Y_D_start1,X_E_start1,Y_E_start1,X_F_start1,Y_F_start1,X_G_start1,Y_G_start1,X_A_stop1,Y_A_stop1,X_B_stop1,Y_B_stop1, X_C_stop1, Y_C_stop1,X_D_stop1,Y_D_stop1,X_E_stop1,Y_E_stop1,X_F_stop1,Y_F_stop1,X_G_stop1,Y_G_stop1,wait_A_start1,wait_AB_start1,wait_B_start1,wait_BC_start1, wait_C_start1,wait_CD_start1,wait_D_start1,wait_DE_start1,wait_E_start1,wait_EF_start1,wait_F_start1,wait_FG_start1,wait_G_start1,wait_A_stop1,wait_AB_stop1,wait_B_stop1,wait_BC_stop1,wait_C_stop1,wait_CD_stop1,wait_D_stop1,wait_DE_stop1,wait_E_stop1,wait_EF_stop1,wait_F_stop1,wait_FG_stop1,wait_G_stop1,N_step_amp1,N_step_wait1,X_A_start2,Y_A_start2,X_B_start2,Y_B_start2, X_C_start2, Y_C_start2,X_D_start2,Y_D_start2,X_E_start2,Y_E_start2,X_F_start2,Y_F_start2,X_G_start2,Y_G_start2,X_A_stop2,Y_A_stop2,X_B_stop2,Y_B_stop2, X_C_stop2, Y_C_stop2,X_D_stop2,Y_D_stop2,X_E_stop2,Y_E_stop2,X_F_stop2,Y_F_stop2,X_G_stop2,Y_G_stop2,wait_A_start2,wait_AB_start2,wait_B_start2,wait_BC_start2, wait_C_start2,wait_CD_start2,wait_D_start2,wait_DE_start2,wait_E_start2,wait_EF_start2,wait_F_start2,wait_FG_start2,wait_G_start2,wait_A_stop2,wait_AB_stop2,wait_B_stop2,wait_BC_stop2,wait_C_stop2,wait_CD_stop2,wait_D_stop2,wait_DE_stop2,wait_E_stop2,wait_EF_stop2,wait_F_stop2,wait_FG_stop2,wait_G_stop2,N_step_amp2,N_step_wait2):



###################################
#########     TO TEST     #########
###################################



db_atenuation_blue=db_atenuation_green=db_atenuation_red=1;
db_atenuation_black=1;

waitA1=0;
waitA2=0;
waitT1=0;
waitT2=0;


###### 1  ######


X_A_start1=-0.01*db_atenuation_black/2;
X_B_start1=-0.02*db_atenuation_black/2;
X_C_start1=-0.03*db_atenuation_black/2;
X_D_start1=-0.04*db_atenuation_black/2;
X_E_start1=-0.05*db_atenuation_black/2;
X_F_start1=-0.06*db_atenuation_black/2;
X_G_start1=-0.07*db_atenuation_black/2;


X_A_stop1=-0.07*db_atenuation_black/2;
X_B_stop1=-0.06*db_atenuation_black/2;
X_C_stop1=-0.05*db_atenuation_black/2;
X_D_stop1=-0.04*db_atenuation_black/2;
X_E_stop1=-0.03*db_atenuation_black/2;
X_F_stop1=-0.02*db_atenuation_black/2;
X_G_stop1=-0.01*db_atenuation_black/2;





Y_A_start1=-0.1*db_atenuation_black/2;
Y_B_start1=-0.2*db_atenuation_black/2;
Y_C_start1=-0.3*db_atenuation_black/2;
Y_D_start1=-0.4*db_atenuation_black/2;
Y_E_start1=-0.5*db_atenuation_black/2;
Y_F_start1=-0.6*db_atenuation_black/2;
Y_G_start1=-0.7*db_atenuation_black/2;


Y_A_stop1=-0.7*db_atenuation_black/2;
Y_B_stop1=-0.6*db_atenuation_black/2;
Y_C_stop1=-0.5*db_atenuation_black/2;
Y_D_stop1=-0.4*db_atenuation_black/2;
Y_E_stop1=-0.3*db_atenuation_black/2;
Y_F_stop1=-0.2*db_atenuation_black/2;
Y_G_stop1=-0.1*db_atenuation_black/2;



wait_A_start1=10e-6
wait_AB_start1=10e-9
wait_B_start1=10e-9
wait_BC_start1=10e-9
wait_C_start1=10e-9
wait_CD_start1=10e-9
wait_D_start1=10e-9
wait_DE_start1=10e-9
wait_E_start1=10e-9
wait_EF_start1=10e-9
wait_F_start1=10e-9
wait_FG_start1=10e-9
wait_G_start1=10e-9

wait_A_stop1=10e-6
wait_AB_stop1=10e-9
wait_B_stop1=10e-9
wait_BC_stop1=10e-9
wait_C_stop1=10e-9
wait_CD_stop1=10e-9
wait_D_stop1=10e-9
wait_DE_stop1=10e-9
wait_E_stop1=10e-9
wait_EF_stop1=10e-9
wait_F_stop1=10e-9
wait_FG_stop1=10e-9
wait_G_stop1=10e-9


N_step_amp1=5
N_step_wait1=0



###### 2  ######


X_A_start2=-0.01*db_atenuation_black/2;
X_B_start2=-0.02*db_atenuation_black/2;
X_C_start2=-0.03*db_atenuation_black/2;
X_D_start2=-0.04*db_atenuation_black/2;
X_E_start2=-0.05*db_atenuation_black/2;
X_F_start2=-0.06*db_atenuation_black/2;
X_G_start2=-0.07*db_atenuation_black/2;


X_A_stop2=-0.07*db_atenuation_black/2;
X_B_stop2=-0.06*db_atenuation_black/2;
X_C_stop2=-0.05*db_atenuation_black/2;
X_D_stop2=-0.04*db_atenuation_black/2;
X_E_stop2=-0.03*db_atenuation_black/2;
X_F_stop2=-0.02*db_atenuation_black/2;
X_G_stop2=-0.01*db_atenuation_black/2;




Y_A_start2=-0.01*db_atenuation_black/2;
Y_B_start2=-0.02*db_atenuation_black/2;
Y_C_start2=-0.03*db_atenuation_black/2;
Y_D_start2=-0.04*db_atenuation_black/2;
Y_E_start2=-0.05*db_atenuation_black/2;
Y_F_start2=-0.06*db_atenuation_black/2;
Y_G_start2=-0.07*db_atenuation_black/2;


Y_A_stop2=-0.07*db_atenuation_black/2;
Y_B_stop2=-0.06*db_atenuation_black/2;
Y_C_stop2=-0.05*db_atenuation_black/2;
Y_D_stop2=-0.04*db_atenuation_black/2;
Y_E_stop2=-0.03*db_atenuation_black/2;
Y_F_stop2=-0.02*db_atenuation_black/2;
Y_G_stop2=-0.01*db_atenuation_black/2;




wait_A_start2=5e-9;
wait_AB_start2=5e-9;
wait_B_start2=5e-9;
wait_BC_start2=5e-9;
wait_C_start2=5e-9;
wait_CD_start2=5e-9;
wait_D_start2=5e-9;
wait_DE_start2=5e-9;
wait_E_start2=5e-9;
wait_EF_start2=5e-9;
wait_F_start2=5e-9;
wait_FG_start2=5e-9;
wait_G_start2=5e-9;

wait_A_stop2=10e-9
wait_AB_stop2=10e-9
wait_B_stop2=10e-9
wait_BC_stop2=10e-9
wait_C_stop2=10e-9
wait_CD_stop2=10e-9
wait_D_stop2=10e-9
wait_DE_stop2=10e-9
wait_E_stop2=10e-9
wait_EF_stop2=10e-9
wait_F_stop2=10e-9
wait_FG_stop2=10e-9
wait_G_stop2=10e-9


N_step_amp2=0

N_step_wait2=0



###########################################


Nindex=1
ADC_samplingrate = 1.0e6;
#AWG_samplingrate = 1.0e7;

AWG_samplingrate = 1.0e9;


decimal=9    ####precision of the waiting time for example for a ns precision decimal=9 for 0.1us decimal=7
trigg_length = 1* AWG_samplingrate/ADC_samplingrate;   # translate the sampling rate of the AWG in number of point related to the sampling rate of the ADC
trigg_period = 1*trigg_length   # define the period of a trigg, related to the triggering of the ADC. With ADC trigg period=2*trigglength (one up and one down). With the LeCroy trigg period =1trigg length (just say to the LeCroy when it starts to measure, can do the same with the ADC)
Nrepeat=1



#
#deltat_A1 = (wait_A_stop1-wait_A_start1)
#deltat_AB1 = (wait_AB_stop1-wait_AB_start1)
#deltat_B1 = (wait_B_stop1-wait_B_start1)
#deltat_BC1 = (wait_BC_stop1-wait_BC_start1)
#deltat_C1 = (wait_C_stop1-wait_C_start1)
#deltat_CD1 = (wait_CD_stop1-wait_CD_start1)
#deltat_D1 = (wait_D_stop1-wait_D_start1)
#deltat_DE1 = (wait_DE_stop1-wait_DE_start1)
#deltat_E1 = (wait_E_stop1-wait_E_start1)
#deltat_EF1 = (wait_EF_stop1-wait_EF_start1)
#deltat_F1 = (wait_F_stop1-wait_F_start1)
#deltat_FG1 = (wait_FG_stop1-wait_FG_start1)
#deltat_G1 = (wait_G_stop1-wait_G_start1)
#
#
#deltat_A2 = (wait_A_stop2-wait_A_start2)
#deltat_AB2 = (wait_AB_stop2-wait_AB_start2)
#deltat_B2 = (wait_B_stop1-wait_B_start2)
#deltat_BC2 = (wait_BC_stop2-wait_BC_start2)
#deltat_C2 = (wait_C_stop2-wait_C_start2)
#deltat_CD2 = (wait_CD_stop2-wait_CD_start2)
#deltat_D2 = (wait_D_stop2-wait_D_start2)
#deltat_DE2 = (wait_DE_stop2-wait_DE_start2)
#deltat_E2 = (wait_E_stop2-wait_E_start2)
#deltat_EF2 = (wait_EF_stop2-wait_EF_start2)
#deltat_F2 = (wait_F_stop2-wait_F_start2)
#deltat_FG2 = (wait_FG_stop2-wait_FG_start2)
#deltat_G2 = (wait_G_stop2-wait_G_start2)
#

deltat1=(wait_A_start1+wait_B_start1+wait_C_start1+wait_D_start1+wait_E_start1+wait_AB_start1+wait_BC_start1+wait_CD_start1+wait_DE_start1+wait_EF_start1+wait_F_start1+wait_G_start1+wait_FG_start1)-(wait_A_stop1+wait_B_stop1+wait_C_stop1+wait_D_stop1+wait_E_stop1+wait_AB_stop1+wait_BC_stop1+wait_CD_stop1+wait_DE_stop1+wait_F_stop1+wait_EF_stop1+wait_FG_stop1+wait_G_stop1)


if deltat1<0:    # =stop>start
    wait_A1_size = int(np.around(wait_A_stop1 * ADC_samplingrate * trigg_period));
    wait_B1_size = int(np.around(wait_B_stop1 * ADC_samplingrate * trigg_period));
    wait_C1_size = int(np.around(wait_C_stop1 * ADC_samplingrate * trigg_period));
    wait_D1_size = int(np.around(wait_D_stop1 * ADC_samplingrate * trigg_period));
    wait_E1_size = int(np.around(wait_E_stop1 * ADC_samplingrate * trigg_period));
    wait_F1_size = int(np.around(wait_F_stop1 * ADC_samplingrate * trigg_period));
    wait_G1_size =int( np.around(wait_G_stop1 * ADC_samplingrate * trigg_period));
    wait_AB1_size =int( np.around(wait_AB_stop1 * ADC_samplingrate * trigg_period));
    wait_BC1_size =int( np.around(wait_BC_stop1 * ADC_samplingrate * trigg_period));
    wait_CD1_size =int( np.around(wait_CD_stop1 * ADC_samplingrate * trigg_period));
    wait_DE1_size =int( np.around(wait_DE_stop1 * ADC_samplingrate * trigg_period));
    wait_EF1_size =int( np.around(wait_EF_stop1 * ADC_samplingrate * trigg_period));
    wait_FG1_size = int(np.around(wait_FG_stop1 * ADC_samplingrate * trigg_period));
    deltat1_size = int(np.around(-deltat1 * ADC_samplingrate * trigg_period));  #size of the difference in time between start and stop
else:
    wait_A1_size = int(np.around(wait_A_start1 * ADC_samplingrate * trigg_period));
    wait_B1_size = int(np.around(wait_B_start1 * ADC_samplingrate * trigg_period));
    wait_C1_size = int(np.around(wait_C_start1 * ADC_samplingrate * trigg_period));
    wait_D1_size = int(np.around(wait_D_start1 * ADC_samplingrate * trigg_period));
    wait_E1_size = int(np.around(wait_E_start1 * ADC_samplingrate * trigg_period));
    wait_F1_size =int( np.around(wait_F_start1 * ADC_samplingrate * trigg_period));
    wait_G1_size =int( np.around(wait_G_start1 * ADC_samplingrate * trigg_period));
    wait_AB1_size =int( np.around(wait_AB_start1 * ADC_samplingrate * trigg_period));
    wait_BC1_size =int( np.around(wait_BC_start1 * ADC_samplingrate * trigg_period));
    wait_CD1_size =int( np.around(wait_CD_start1 * ADC_samplingrate * trigg_period));
    wait_DE1_size =int( np.around(wait_DE_start1 * ADC_samplingrate * trigg_period));
    wait_EF1_size =int( np.around(wait_EF_start1 * ADC_samplingrate * trigg_period));
    wait_FG1_size =int( np.around(wait_FG_start1 * ADC_samplingrate * trigg_period));
    deltat1_size = int(np.around(deltat1 * ADC_samplingrate * trigg_period));
    
    
#    
#delta_A1_X= (X_A_stop1-X_A_start1)
#delta_A1_Y= (Y_A_stop1-Y_A_start1)
#
#delta_B1_X= (X_B_stop1-X_B_start1)
#delta_B1_Y= (Y_B_stop1-Y_B_start1)
#
#delta_C1_X= (X_C_stop1-X_C_start1)
#delta_C1_Y= (Y_C_stop1-Y_C_start1)
#
#delta_D1_X= (X_D_stop1-X_D_start1)
#delta_D1_Y= (Y_D_stop1-Y_D_start1)
#
#delta_E1_X= (X_E_stop1-X_E_start1)
#delta_E1_Y= (Y_E_stop1-Y_E_start1)
#
#delta_F1_X= (X_F_stop1-X_F_start1)
#delta_F1_Y= (Y_F_stop1-Y_F_start1)
#
#delta_G1_X= (X_G_stop1-X_G_start1)
#delta_G1_Y= (Y_G_stop1-Y_G_start1)


if N_step_amp1==0 and N_step_wait1==0:
    scan_length1=0
else:
    scan_length1= int((wait_A1_size+wait_B1_size+wait_C1_size+wait_D1_size+wait_E1_size+wait_F1_size+wait_G1_size+wait_AB1_size+wait_BC1_size+wait_CD1_size+wait_DE1_size+wait_EF1_size+wait_FG1_size) + waitA1+waitT1);


deltat2=(wait_A_start2+wait_B_start2+wait_C_start2+wait_D_start2+wait_E_start2+wait_AB_start2+wait_BC_start2+wait_CD_start2+wait_DE_start2+wait_EF_start2+wait_F_start2+wait_G_start2+wait_FG_start2)-(wait_A_stop2+wait_B_stop2+wait_C_stop2+wait_D_stop2+wait_E_stop2+wait_AB_stop2+wait_BC_stop2+wait_CD_stop2+wait_DE_stop2+wait_F_stop2+wait_EF_stop2+wait_FG_stop2+wait_G_stop2)


if deltat2<0:    # =stop>start
    wait_A2_size = int(np.around(wait_A_stop2 * ADC_samplingrate * trigg_period));
    wait_B2_size = int(np.around(wait_B_stop2 * ADC_samplingrate * trigg_period));
    wait_C2_size = int(np.around(wait_C_stop2 * ADC_samplingrate * trigg_period));
    wait_D2_size = int(np.around(wait_D_stop2 * ADC_samplingrate * trigg_period));
    wait_E2_size = int(np.around(wait_E_stop2 * ADC_samplingrate * trigg_period));
    wait_F2_size = int(np.around(wait_F_stop2 * ADC_samplingrate * trigg_period));
    wait_G2_size =int( np.around(wait_G_stop2 * ADC_samplingrate * trigg_period));
    wait_AB2_size =int( np.around(wait_AB_stop2 * ADC_samplingrate * trigg_period));
    wait_BC2_size =int( np.around(wait_BC_stop2 * ADC_samplingrate * trigg_period));
    wait_CD2_size =int( np.around(wait_CD_stop2 * ADC_samplingrate * trigg_period));
    wait_DE2_size =int( np.around(wait_DE_stop2 * ADC_samplingrate * trigg_period));
    wait_EF2_size =int( np.around(wait_EF_stop2 * ADC_samplingrate * trigg_period));
    wait_FG2_size = int(np.around(wait_FG_stop2 * ADC_samplingrate * trigg_period));
    deltat2_size = int(np.around(-deltat2 * ADC_samplingrate * trigg_period));  #size of the difference in time between start and stop
else:
    wait_A2_size = int(np.around(wait_A_start2 * ADC_samplingrate * trigg_period));
    wait_B2_size = int(np.around(wait_B_start2 * ADC_samplingrate * trigg_period));
    wait_C2_size = int(np.around(wait_C_start2 * ADC_samplingrate * trigg_period));
    wait_D2_size = int(np.around(wait_D_start2 * ADC_samplingrate * trigg_period));
    wait_E2_size = int(np.around(wait_E_start2 * ADC_samplingrate * trigg_period));
    wait_F2_size =int( np.around(wait_F_start2 * ADC_samplingrate * trigg_period));
    wait_G2_size =int( np.around(wait_G_start2 * ADC_samplingrate * trigg_period));
    wait_AB2_size =int( np.around(wait_AB_start2 * ADC_samplingrate * trigg_period));
    wait_BC2_size =int( np.around(wait_BC_start2 * ADC_samplingrate * trigg_period));
    wait_CD2_size =int( np.around(wait_CD_start2 * ADC_samplingrate * trigg_period));
    wait_DE2_size =int( np.around(wait_DE_start2 * ADC_samplingrate * trigg_period));
    wait_EF2_size =int( np.around(wait_EF_start2 * ADC_samplingrate * trigg_period));
    wait_FG2_size =int( np.around(wait_FG_start2 * ADC_samplingrate * trigg_period));
    deltat2_size = int(np.around(deltat2 * ADC_samplingrate * trigg_period));


#delta_A2_X= (X_A_stop2-X_A_start2)
#delta_A2_Y= (Y_A_stop2-Y_A_start2)
#
#delta_B2_X= (X_B_stop2-X_B_start2)
#delta_B2_Y= (Y_B_stop2-Y_B_start2)
#
#delta_C2_X= (X_C_stop2-X_C_start2)
#delta_C2_Y= (Y_C_stop2-Y_C_start2)
#
#delta_D2_X= (X_D_stop2-X_D_start2)
#delta_D2_Y= (Y_D_stop2-Y_D_start2)
#
#delta_E2_X= (X_E_stop2-X_E_start2)
#delta_E2_Y= (Y_E_stop2-Y_E_start2)
#
#delta_F2_X= (X_F_stop2-X_F_start2)
#delta_F2_Y= (Y_F_stop2-Y_F_start2)
#
#delta_G2_X= (X_G_stop2-X_G_start2)
#delta_G2_Y= (Y_G_stop2-Y_G_start2)
#   
#   
if N_step_amp2==0 and N_step_wait2==0:
    scan_length2=0
else: 
    scan_length2= int((wait_A2_size+wait_B2_size+wait_C2_size+wait_D2_size+wait_E2_size+wait_F2_size+wait_G2_size+wait_AB2_size+wait_BC2_size+wait_CD2_size+wait_DE2_size+wait_EF2_size+wait_FG2_size) + waitA2+waitT2);#length of a complete scan, with the ramp, steps, security ramp, etc


scan_length=scan_length1+scan_length2;

N_step=N_step_amp2+N_step_wait2+N_step_amp1+N_step_wait1

########################################
#       INITIALISATION
########################################



###### complete 
C1_DATA=np.zeros((Nindex+N_step,scan_length));
C2_DATA=np.zeros((Nindex+N_step,scan_length));
C3_DATA=np.zeros((Nindex+N_step,scan_length));
C4_DATA=np.zeros((Nindex+N_step,scan_length));

MARKER_C1_1=np.zeros((Nindex+N_step,scan_length));
MARKER_C2_1=np.zeros((Nindex+N_step,scan_length));
MARKER_C3_1=np.zeros((Nindex+N_step,scan_length));
MARKER_C4_1=np.zeros((Nindex+N_step,scan_length));

MARKER_C1_2=np.zeros((Nindex+N_step,scan_length));
MARKER_C2_2=np.zeros((Nindex+N_step,scan_length));
MARKER_C3_2=np.zeros((Nindex+N_step,scan_length));
MARKER_C4_2=np.zeros((Nindex+N_step,scan_length));

JUMPS_DATA=np.zeros((Nindex+N_step,4));
AMPLITUDE=np.zeros((N_step+Nindex,4))
OFFSET=np.zeros((N_step+Nindex,4))
SIZE=np.zeros((1,N_step+Nindex))


##### amplitude1 

C1A1=np.zeros((Nindex+N_step_amp1,scan_length));
C2A1=np.zeros((Nindex+N_step_amp1,scan_length));
C3A1=np.zeros((Nindex+N_step_amp1,scan_length));
C4A1=np.zeros((Nindex+N_step_amp1,scan_length));

M_C1_1A1=np.zeros((Nindex+N_step_amp1,scan_length));
M_C2_1A1=np.zeros((Nindex+N_step_amp1,scan_length));
M_C3_1A1=np.zeros((Nindex+N_step_amp1,scan_length));
M_C4_1A1=np.zeros((Nindex+N_step_amp1,scan_length));

M_C1_2A1=np.zeros((Nindex+N_step_amp1,scan_length));
M_C2_2A1=np.zeros((Nindex+N_step_amp1,scan_length));
M_C3_2A1=np.zeros((Nindex+N_step_amp1,scan_length));
M_C4_2A1=np.zeros((Nindex+N_step_amp1,scan_length));

JUMPS_DA1=np.zeros((Nindex+N_step_amp1,4));
AMPA1=np.zeros((N_step+N_step_amp1,4))
OFFSA1=np.zeros((N_step+N_step_amp1,4))
SIZA1=np.zeros((1,N_step+N_step_amp1))





 ##### waiting time1 

C1T1=np.zeros((Nindex+N_step_wait1,scan_length));
C2T1=np.zeros((Nindex+N_step_wait1,scan_length));
C3T1=np.zeros((Nindex+N_step_wait1,scan_length));
C4T1=np.zeros((Nindex+N_step_wait1,scan_length));

M_C1_1T1=np.zeros((Nindex+N_step_wait1,scan_length));
M_C2_1T1=np.zeros((Nindex+N_step_wait1,scan_length));
M_C3_1T1=np.zeros((Nindex+N_step_wait1,scan_length));
M_C4_1T1=np.zeros((Nindex+N_step_wait1,scan_length));

M_C1_2T1=np.zeros((Nindex+N_step_wait1,scan_length));
M_C2_2T1=np.zeros((Nindex+N_step_wait1,scan_length));
M_C3_2T1=np.zeros((Nindex+N_step_wait1,scan_length));
M_C4_2T1=np.zeros((Nindex+N_step_wait1,scan_length));

JUMPS_DT1=np.zeros((Nindex+N_step_wait1,4));
AMPT1=np.zeros((N_step+N_step_wait1,4))
OFFST1=np.zeros((N_step+N_step_wait1,4))
SIZT1=np.zeros((1,N_step+N_step_wait1))


 
##### amplitude2

C1A2=np.zeros((Nindex+N_step_amp2,scan_length));
C2A2=np.zeros((Nindex+N_step_amp2,scan_length));
C3A2=np.zeros((Nindex+N_step_amp2,scan_length));
C4A2=np.zeros((Nindex+N_step_amp2,scan_length));

M_C1_1A2=np.zeros((Nindex+N_step_amp2,scan_length));
M_C2_1A2=np.zeros((Nindex+N_step_amp2,scan_length));
M_C3_1A2=np.zeros((Nindex+N_step_amp2,scan_length));
M_C4_1A2=np.zeros((Nindex+N_step_amp2,scan_length));

M_C1_2A2=np.zeros((Nindex+N_step_amp2,scan_length));
M_C2_2A2=np.zeros((Nindex+N_step_amp2,scan_length));
M_C3_2A2=np.zeros((Nindex+N_step_amp2,scan_length));
M_C4_2A2=np.zeros((Nindex+N_step_amp2,scan_length));

JUMPS_DA2=np.zeros((Nindex+N_step_amp2,4));
AMPA2=np.zeros((N_step+N_step_amp2,4))
OFFSA2=np.zeros((N_step+N_step_amp2,4))
SIZA2=np.zeros((1,N_step+N_step_amp2))  


  

##### waiting time2
C1T2=np.zeros((Nindex+N_step_wait2,scan_length));
C2T2=np.zeros((Nindex+N_step_wait2,scan_length));
C3T2=np.zeros((Nindex+N_step_wait2,scan_length));
C4T2=np.zeros((Nindex+N_step_wait2,scan_length));

M_C1_1T2=np.zeros((Nindex+N_step_wait2,scan_length));
M_C2_1T2=np.zeros((Nindex+N_step_wait2,scan_length));
M_C3_1T2=np.zeros((Nindex+N_step_wait2,scan_length));
M_C4_1T2=np.zeros((Nindex+N_step_wait2,scan_length));

M_C1_2T2=np.zeros((Nindex+N_step_wait2,scan_length));
M_C2_2T2=np.zeros((Nindex+N_step_wait2,scan_length));
M_C3_2T2=np.zeros((Nindex+N_step_wait2,scan_length));
M_C4_2T2=np.zeros((Nindex+N_step_wait2,scan_length));

JUMPS_DT2=np.zeros((Nindex+N_step_wait2,4));
AMPT2=np.zeros((N_step+N_step_wait2,4))
OFFST2=np.zeros((N_step+N_step_wait2,4))
SIZT2=np.zeros((1,N_step+N_step_wait2)) 





########################################
#       AMPLITUDE
########################################



if N_step_amp1>0:
    ### defined with wait_start=wait_stop then offer the possibility to change twice the amplitude and wait
    C1A1,C2A1,C3A1,C4A1,JUMPS_DA1,SIZA1,M_C1_1A1,M_C2_1A1,M_C3_1A1,M_C4_1A1,M_C1_2A1,M_C2_2A1,M_C3_2A1,M_C4_2A1,AMPA1,OFFSA1=multi_rabi_amplitude(X_A_start1,Y_A_start1,X_B_start1,Y_B_start1, X_C_start1, Y_C_start1,X_D_start1,Y_D_start1,X_E_start1,Y_E_start1,X_F_start1,Y_F_start1,X_G_start1,Y_G_start1,X_A_stop1,Y_A_stop1,X_B_stop1,Y_B_stop1, X_C_stop1, Y_C_stop1,X_D_stop1,Y_D_stop1,X_E_stop1,Y_E_stop1,X_F_stop1,Y_F_stop1,X_G_stop1,Y_G_stop1,wait_A_start1,wait_AB_start1,wait_B_start1,wait_BC_start1, wait_C_start1,wait_CD_start1,wait_D_start1,wait_DE_start1,wait_E_start1,wait_EF_start1,wait_F_start1,wait_FG_start1,wait_G_start1,wait_A_start1,wait_AB_start1,wait_B_start1,wait_BC_start1, wait_C_start1,wait_CD_start1,wait_D_start1,wait_DE_start1,wait_E_start1,wait_EF_start1,wait_F_start1,wait_FG_start1,wait_G_start1,N_step_amp1)
    
    wait_tot1 = int(((wait_A_start1+wait_AB_start1+wait_B_start1+wait_BC_start1+ wait_C_start1+wait_CD_start1+wait_D_start1+wait_DE_start1+wait_E_start1+wait_EF_start1+wait_F_start1+wait_FG_start1+wait_G_start1))* ADC_samplingrate * trigg_period)

   
#    
    C1A1=np.delete(C1A1,(0),axis=0)
    C1A1=np.delete(C1A1,(-1),axis=0)
       
    C2A1=np.delete(C2A1,(0),axis=0)
    C2A1=np.delete(C2A1,(-1),axis=0)
       
    C3A1=np.delete(C3A1,(0),axis=0)
    C3A1=np.delete(C3A1,(-1),axis=0)
       
    C4A1=np.delete(C4A1,(0),axis=0)
    C4A1=np.delete(C4A1,(-1),axis=0)


    C1_DATA[0:N_step_amp1][0:wait_tot1]=C1A1[:]
    C1_DATA[0:N_step_amp1][wait_tot1:]=C1A1[:][-1]
  
    C2_DATA[0:N_step_amp1][0:wait_tot1]=C2A1[:]
    C2_DATA[0:N_step_amp1][wait_tot1:]=C2A1[:][-1]
    
    C3_DATA[0:N_step_amp1][0:wait_tot1]=C3A1[:]
    C3_DATA[0:N_step_amp1][wait_tot1:]=C3A1[:][-1]
    
    C4_DATA[0:N_step_amp1][0:wait_tot1]=C4A1[:]
    C4_DATA[0:N_step_amp1][wait_tot1:]=C4A1[:][-1]
          
    M_C1_1A1=np.delete(M_C1_1A1,(0),axis=0)
    M_C1_1A1=np.delete(M_C1_1A1,(-1),axis=0)
       
    M_C2_1A1=np.delete(M_C2_1A1,(0),axis=0)
    M_C2_1A1=np.delete(M_C2_1A1,(-1),axis=0)
       
    M_C3_1A1=np.delete(M_C3_1A1,(0),axis=0)
    M_C3_1A1=np.delete(M_C3_1A1,(-1),axis=0)
       
    M_C4_1A1=np.delete(M_C4_1A1,(0),axis=0)
    M_C4_1A1=np.delete(M_C4_1A1,(-1),axis=0)
     
    
    MARKER_C1_1[0:N_step_amp1][0:wait_tot1]=M_C1_1A1[:]
    MARKER_C2_1[0:N_step_amp1][0:wait_tot1]=M_C2_1A1[:]
    MARKER_C3_1[0:N_step_amp1][0:wait_tot1]=M_C3_1A1[:]
    MARKER_C4_1[0:N_step_amp1][0:wait_tot1]=M_C4_1A1[:]
    
    
    M_C1_2A1=np.delete(M_C1_2A1,(0),axis=0)
    M_C1_2A1=np.delete(M_C1_2A1,(-1),axis=0)
       
    M_C2_2A1=np.delete(M_C2_2A1,(0),axis=0)
    M_C2_2A1=np.delete(M_C2_2A1,(-1),axis=0)
       
    M_C3_2A1=np.delete(M_C3_2A1,(0),axis=0)
    M_C3_2A1=np.delete(M_C3_2A1,(-1),axis=0)
       
    M_C4_2A1=np.delete(M_C4_2A1,(0),axis=0)
    M_C4_2A1=np.delete(M_C4_2A1,(-1),axis=0)
    
    
    MARKER_C1_2[0:N_step_amp1][0:wait_tot1]=M_C1_2A1[:]
    MARKER_C2_2[0:N_step_amp1][0:wait_tot1]=M_C2_2A1[:]
    MARKER_C3_2[0:N_step_amp1][0:wait_tot1]=M_C3_2A1[:]
    MARKER_C4_2[0:N_step_amp1][0:wait_tot1]=M_C4_2A1[:]





for i in range(0,N_step):
#        
        plt.figure(2)
        plt.plot(C1_DATA[i+1][:])
#        plt.plot(MARKER_C1_1[1]-1)
    
        plt.figure(1) 
        plt.plot(C2_DATA[i+1][:])
    
    
    
########################################
#       WAITING TIME
######################################## 
    
    
    
    
if N_step_wait1>0:
    
    ## defined with A,B,C,D,E,F,G start values
    C1T1,C2AT1,C3T1,C4T1,JUMPS_DT1,SIZT1,M_C1_1T1,M_C2_1T1,M_C3_1T1,M_C4_1T1,M_C1_2T1,M_C2_2T1,M_C3_2T1,M_C4_2T1,AMPT1,OFFST1=multi_rabi_waitingtime(X_A_start1,Y_A_start1,X_B_start1,Y_B_start1, X_C_start1, Y_C_start1,X_D_start1,Y_D_start1,X_E_start1,Y_E_start1,X_F_start1,Y_F_start1,X_G_start1,Y_G_start1,wait_A_start1,wait_AB_start1,wait_B_start1,wait_BC_start1, wait_C_start1,wait_CD_start1,wait_D_start1,wait_DE_start1,wait_E_start1,wait_EF_start1,wait_F_start1,wait_FG_start1,wait_G_start1,wait_A_stop1,wait_AB_stop1,wait_B_stop1,wait_BC_stop1,wait_C_stop1,wait_CD_stop1,wait_D_stop1,wait_DE_stop1,wait_E_stop1,wait_EF_stop1,wait_F_stop1,wait_FG_stop1,wait_G_stop1,N_step_wait1)

    for i in range(0,N_step_wait1):
        
        wait_tot3=C1T1[i][:].size;
        
        C1_DATA[N_step_amp1+i][0:wait_tot3]=C1T1[i]
        C1_DATA[N_step_amp1+i][wait_tot3:]=C1T1[i][-1]
      
        C2_DATA[N_step_amp1+i][0:wait_tot3]=C2T1[i]
        C2_DATA[N_step_amp1+i][wait_tot3:]=C2T1[i][-1]
        
        C3_DATA[N_step_amp1+i][0:wait_tot3]=C3T1[i]
        C3_DATA[N_step_amp1+i][wait_tot3:]=C3T1[i][-1]
        
        C4_DATA[N_step_amp1+i][0:wait_tot3]=C4T1[i]
        C4_DATA[N_step_amp1+i][wait_tot3:]=C4T1[i][-1]
              
        MARKER_C1_1[N_step_amp1+i][0:wait_tot3]=M_C1_1T1[i]
        MARKER_C2_1[N_step_amp1+i][0:wait_tot3]=M_C2_1T1[i]
        MARKER_C3_1[N_step_amp1+i][0:wait_tot3]=M_C3_1T1[i]
        MARKER_C4_1[N_step_amp1+i][0:wait_tot3]=M_C4_1T1[i]
        
        MARKER_C1_2[N_step_amp1+i][0:wait_tot3]=M_C1_2T1[i]
        MARKER_C2_2[N_step_amp1+i][0:wait_tot3]=M_C2_2T1[i]
        MARKER_C3_2[N_step_amp1+i][0:wait_tot3]=M_C3_2T1[i]
        MARKER_C4_2[N_step_amp1+i][0:wait_tot3]=M_C4_2T1[i]




###################################################
#####
#
#####                   2
#
#####
###################################################

















if N_step_amp2>0:
    ### defined with wait_start=wait_stop then offer the possibility to change twice the amplitude and wait
    C1A2,C2A2,C3A2,C4A2,JUMPS_DA2,SIZA2,M_C1_1A2,M_C2_1A2,M_C3_1A2,M_C4_1A2,M_C1_2A2,M_C2_2A2,M_C3_2A2,M_C4_2A2,AMPA2,OFFSA2=multi_rabi_amplitude(X_A_start2,Y_A_start2,X_B_start2,Y_B_start2, X_C_start2, Y_C_start2,X_D_start2,Y_D_start2,X_E_start2,Y_E_start2,X_F_start2,Y_F_start2,X_G_start2,Y_G_start2,X_A_stop2,Y_A_stop2,X_B_stop2,Y_B_stop2, X_C_stop2, Y_C_stop2,X_D_stop2,Y_D_stop2,X_E_stop2,Y_E_stop2,X_F_stop2,Y_F_stop2,X_G_stop2,Y_G_stop2,wait_A_start2,wait_AB_start2,wait_B_start2,wait_BC_start2, wait_C_start2,wait_CD_start2,wait_D_start2,wait_DE_start2,wait_E_start2,wait_EF_start2,wait_F_start2,wait_FG_start2,wait_G_start2,wait_A_start2,wait_AB_start2,wait_B_start2,wait_BC_start2, wait_C_start2,wait_CD_start2,wait_D_start2,wait_DE_start2,wait_E_start2,wait_EF_start2,wait_F_start2,wait_FG_start2,wait_G_start2,N_step_amp2)
    
    wait_tot2 = ((wait_A_start2+wait_AB_start2+wait_B_start2+wait_BC_start2+ wait_C_start2+wait_CD_start2+wait_D_start2+wait_DE_start2+wait_E_start2+wait_EF_start2+wait_F_start2+wait_FG_start2+wait_G_start2))* ADC_samplingrate * trigg_period

    C1_DATA[N_step_wait1:N_step_amp2][0:wait_tot2]=C1A2[:]
    C1_DATA[N_step_wait1:N_step_amp2][wait_tot2:]=C1A2[:][-1]
  
    C2_DATA[N_step_wait1:N_step_amp2][0:wait_tot2]=C2A2[:]
    C2_DATA[N_step_wait1:N_step_amp2][wait_tot2:]=C2A2[:][-1]
    
    C3_DATA[N_step_wait1:N_step_amp2][0:wait_tot2]=C3A2[:]
    C3_DATA[N_step_wait1:N_step_amp2][wait_tot2:]=C3A2[:][-1]
    
    C4_DATA[N_step_wait1:N_step_amp2][0:wait_tot2]=C4A2[:]
    C4_DATA[N_step_wait1:N_step_amp2][wait_tot2:]=C4A2[:][-1]
          
    MARKER_C1_1[N_step_wait1:N_step_amp2][0:wait_tot2]=M_C1_1A2[:]
    MARKER_C2_1[N_step_wait1:N_step_amp2][0:wait_tot2]=M_C2_1A2[:]
    MARKER_C3_1[N_step_wait1:N_step_amp2][0:wait_tot2]=M_C3_1A2[:]
    MARKER_C4_1[N_step_wait1:N_step_amp2][0:wait_tot2]=M_C4_1A2[:]
    
    MARKER_C1_2[N_step_wait1:N_step_amp2][0:wait_tot2]=M_C1_2A2[:]
    MARKER_C2_2[N_step_wait1:N_step_amp2][0:wait_tot2]=M_C2_2A2[:]
    MARKER_C3_2[N_step_wait1:N_step_amp2][0:wait_tot2]=M_C3_2A2[:]
    MARKER_C4_2[N_step_wait1:N_step_amp2][0:wait_tot2]=M_C4_2A2[:]
    
#        SIZE[0][0]=np.shape(C4_DATA)[1];
#        SIZE[0][0:N_step_amp2]=np.shape(C4_DATA)[1];
    
    
    
    
    
    


if N_step_wait2>0:
    
    ## defined with A,B,C,D,E,F,G start values
    C1T2,C2AT2,C3T2,C4T2,JUMPS_DT2,SIZT2,M_C1_1T2,M_C2_1T2,M_C3_1T2,M_C4_1T2,M_C1_2T2,M_C2_2T2,M_C3_2T2,M_C4_2T2,AMPT2,OFFST2=multi_rabi_waitingtime(X_A_start2,Y_A_start2,X_B_start2,Y_B_start2, X_C_start2, Y_C_start2,X_D_start2,Y_D_start2,X_E_start2,Y_E_start2,X_F_start2,Y_F_start2,X_G_start2,Y_G_start2,wait_A_start2,wait_AB_start2,wait_B_start2,wait_BC_start2, wait_C_start2,wait_CD_start2,wait_D_start2,wait_DE_start2,wait_E_start2,wait_EF_start2,wait_F_start2,wait_FG_start2,wait_G_start2,wait_A_stop2,wait_AB_stop2,wait_B_stop2,wait_BC_stop2,wait_C_stop2,wait_CD_stop2,wait_D_stop2,wait_DE_stop2,wait_E_stop2,wait_EF_stop2,wait_F_stop2,wait_FG_stop2,wait_G_stop2,N_step_wait2)

    for i in rang(0,N_step_wait2):
        
        wait_tot4=C1T2[i][:].size;
        
        C1_DATA[N_step_amp2+i][0:wait_tot4]=C1T2[i]
        C1_DATA[N_step_amp2+i][wait_tot4:]=C1T2[i][-1]
      
        C2_DATA[N_step_amp2+i][0:wait_tot4]=C2T2[i]
        C2_DATA[N_step_amp2+i][wait_tot4:]=C2T2[i][-1]
        
        C3_DATA[N_step_amp2+i][0:wait_tot4]=C3T2[i]
        C3_DATA[N_step_amp2+i][wait_tot4:]=C3T2[i][-1]
        
        C4_DATA[N_step_amp2+i][0:wait_tot4]=C4T2[i]
        C4_DATA[N_step_amp2+i][wait_tot4:]=C4T2[i][-1]
              
        MARKER_C1_1[N_step_amp2+i][0:wait_tot4]=M_C1_1T2[i]
        MARKER_C2_1[N_step_amp2+i][0:wait_tot4]=M_C2_1T2[i]
        MARKER_C3_1[N_step_amp2+i][0:wait_tot4]=M_C3_1T2[i]
        MARKER_C4_1[N_step_amp2+i][0:wait_tot4]=M_C4_1T2[i]
        
        MARKER_C1_2[N_step_amp2+i][0:wait_tot4]=M_C1_2T2[i]
        MARKER_C2_2[N_step_amp2+i][0:wait_tot4]=M_C2_2T2[i]
        MARKER_C3_2[N_step_amp2+i][0:wait_tot4]=M_C3_2T2[i]
        MARKER_C4_2[N_step_amp2+i][0:wait_tot4]=M_C4_2T2[i]
    










    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    