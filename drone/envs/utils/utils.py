import math
import numpy as np
def abg_to_ypr(alpha: float, beta: float, gamma: float):
    '''
    Convert alpha, beta and gamma euler angles to roll pitch and yaw
    '''
    aC = math.cos(alpha)
    aS = math.sin(alpha)
    bC = math.cos(beta)
    bS = math.sin(beta)
    gC = math.cos(gamma)
    gS = math.sin(gamma)
    
    m = np.zeros(9,dtype=float)
    m[0] = bC*gC
    m[1] = -bC*gS
    m[2] = bS
    m[3] = aS*bS*gC + aC*gS
    m[4] = -aS*bS*gS + aC*gC
    m[5] = -aS*bC
    m[6] = -aC*bS*gC + bS*gS
    m[7] = aC*bS*gS + bS*gC
    m[8] = aC*gC

    v = m[6]
    if(v > 1):
        v = 1
    elif(v < -1):
        v = -1
    
    pitch = math.asin(-v)
    roll = 0
    yaw = 0
    if(abs(v) < 0.999999):
        roll = math.atan2(m[7],m[8])
        yaw = math.atan2(m[3],m[0])
    else:
        roll = math.atan2(-m[5],m[4])
        yaw = 0
    
    return yaw,pitch,roll