import numpy as np

def Generate_SequenceInfo():
    '''
    SequenceInfo = dict:
        - 'Dimensions' = [n_i, n_j, ...]
        - 'WaitDuration' = waiting element duration
        - 'Elements' = dict:
            - i = dict:
                - 1 = np.array([]) @ current index
                - 2 = np.array([]) @ current index
                - 3 = np.array([]) @ current index
                - 4 = np.array([]) @ current index
                - Duration
                - 'ToNext' (connection to next point) = 'flat'(default), 'linear ramp'
    '''
    SequenceInfo = {} #Init
    SequenceInfo['Dimensions'] = [10] # number of steps
    SequenceInfo['WaitDuration'] = 2000 #Whatever > 1000
    SequenceInfo['Elements'] = {} #Init
    a = np.ones([1.])

    # Waiting at 0
    P0 = {}
    P0[1] = a * 0.
    P0[2] = a * 0.
    P0[3] = a * 0.
    P0[4] = a * 0.
    P0['Duration'] = a * 14000
    P0['ToNext'] = 'flat'
    SequenceInfo['Elements'][0] = P0

    # Transfer TL -> L (TL-L dots)
    P1 = {}
    P1[1] = a * 0.25 * 5.
    P1[2] = a * 0.
    P1[3] = a * 0.
    P1[4] = a * 0.
    P1['Duration'] = a * 6000
    P1['ToNext'] = 'flat'
    SequenceInfo['Elements'][1] = P1

    # Go to L (5dots)
    P2 = {}
    P2[1] = a * 0.25 * 5.
    P2[2] = a * 0.12 * 5.
    P2[3] = a * -0.065 * 5.
    P2[4] = a * 0.18 * 5.
    P2['Duration'] = a * 4000
    P2['ToNext'] = 'flat'
    SequenceInfo['Elements'][2] = P2

    # Pulse for spin mixing (50 ns)
    # Position is stepped
    P3 = {}
    P3[1] = np.linspace(0.25, -0.1, SequenceInfo['Dimensions'][0]) * 5.
    P3[2] = a * 0.12 * 5.
    P3[3] = np.linspace(-0.065, 0.285, SequenceInfo['Dimensions'][0]) * 5.
    P3[4] = a * 0.18 * 5.
    P3['Duration'] = a * 50
    P3['ToNext'] = 'flat'
    SequenceInfo['Elements'][3] = P3

    # Back to L (5dots)
    SequenceInfo['Elements'][4] = P2

    # Go to L (TL-L dots)
    SequenceInfo['Elements'][5] = P1

    # Transfer L -> TL (TL-L dots)
    SequenceInfo['Elements'][6] = P0


    return SequenceInfo
